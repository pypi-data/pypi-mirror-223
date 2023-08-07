#!/usr/bin/env python3

import argparse
import numpy as np
import os
import time

from imagex.problem import ElasticProblem
from imagex.propagator import ElasticPropagator
from imagex.solver import Solver
from imagex.utils import check_shape, load_yaml, print_time, merge_model


class Inversion(object):
    ''' Nonlinear inversion class
    '''

    def __init__(self, parfile, verbose=False):
        ''' Initialize the forward modeling class
        '''

        # load parameters
        params = load_yaml(parfile)

        # load the model
        self.__load_params(params, verbose)

        # analyze the parameters are legal or not
        self.__analyze_params()

        # set the problem and solver
        self.__set_default_inversion()


    def __load_params(self, params, verbose):
        ''' Load the model parameters
        '''

        # convert the dictionary to object attributes
        for _, value in params.items():
            for k, v in value.items():
                setattr(self, k, v)

        # set the parameters list for checking
        para_list = ['data_path', 'nx', 'nz', 'dx', 'dz', 'nt', 'dt', 'f0', 
                     'das_gl', 'npml', 'ngpu', 'weight_pr', 'weight_vx', 
                     'weight_vz', 'weight_et', 'ind_src_file', 'stf_file',
                     'ind_rec_file', 'ind_das_file', 'das_wt_file',
                     'vp_int_file', 'vs_int_file', 'rho_int_file',
                     'niter_max', 'conv', 'method', 'grad_vp_mask_file',
                     'grad_vs_mask_file', 'grad_rho_mask_file',
                     'vp_lb_file', 'vp_ub_file', 'vs_lb_file', 'vs_ub_file',
                     'rho_lb_file', 'rho_ub_file', 'debug', 'output_path']

        # set the default parameters
        if not hasattr(self, 'npml'):
            self.npml = 20
        if not hasattr(self, 'ngpu'):
            self.ngpu = 1
        if not hasattr(self, 'niter_max'):
            self.niter_max = 100
        if not hasattr(self, 'conv'):
            self.conv = 5e-3
        if not hasattr(self, 'method'):
            self.method = 'LBFGS'
        if not hasattr(self, 'debug'):
            self.debug = 'False'
        if not hasattr(self, 'output_path'):
            self.output_path = 'fwi'

        # check the existence of the parameters
        for para in para_list:
            if not hasattr(self, para):
                raise ValueError(f'Inversion: parameter {para} is missing!')

        # print the parameters for debug
        if verbose:
            for para in para_list:
                print(f'{para} = {getattr(self, para)}')

        # set derived parameters
        self.x = np.arange(self.nx) * self.dx + 0.0
        self.z = np.arange(self.nz) * self.dz + 0.0
        self.t = np.arange(self.nt) * self.dt + 0.0

        ind_src = np.load(self.ind_src_file)
        ind_rec = np.load(self.ind_rec_file)
        ind_das = np.load(self.ind_das_file)
        das_wt = np.load(self.das_wt_file)
        stf = np.load(self.stf_file)

        # set the source and receiver
        self.ind_src_x = ind_src[0, :]
        self.ind_src_z = ind_src[1, :]
        self.ind_rec_x = ind_rec[0, :]
        self.ind_rec_z = ind_rec[1, :]
        self.ind_das_x = ind_das[0, :]
        self.ind_das_z = ind_das[1, :]
        self.das_wt_x = das_wt[0, :]
        self.das_wt_z = das_wt[1, :]
        self.stf = stf

        # load the initial model, gradient mask, and the bounds
        par_list = ['vp_int', 'vs_int', 'rho_int', 'vp_lb', 'vp_ub',
                    'vs_lb', 'vs_ub', 'rho_lb', 'rho_ub', 'grad_vp_mask', 
                    'grad_vs_mask', 'grad_rho_mask']

        for par in par_list:
            data = np.load(getattr(self, par + '_file'))
            check_shape(data, (self.nz, self.nx))
            setattr(self, par, data)


    def __analyze_params(self):
        ''' Analyze the parameters are legal to continue the inversion
        '''

        # check the data files
        inv_comp = []

        if self.weight_pr > 0:
            inv_comp.append('pr')
        if self.weight_vx > 0:
            inv_comp.append('vx')
        if self.weight_vz > 0:
            inv_comp.append('vz')
        if self.weight_et > 0:
            inv_comp.append('et')

        nsrc = len(self.ind_src_x)
        for isrc in range(nsrc):
            for comp in inv_comp:
                file = os.path.join(self.data_path, f'shot{isrc}_{comp}.bin')
                if not os.path.exists(file):
                    raise ValueError(f'Inversion: the data file {file} does not exist.')

        # set the output path and clean the output folder
        if os.path.exists(self.output_path):
            os.system(f'rm -rf {self.output_path}')
        os.makedirs(self.output_path, exist_ok=True)


        # check the mask is legal
        if np.any(self.grad_vp_mask < 0) or np.any(self.grad_vs_mask < 0) or np.any(self.grad_rho_mask < 0):
            raise ValueError('Inversion: the mask of the model parameters is negative.')

        if np.any(self.grad_vp_mask > 10) or np.any(self.grad_vs_mask > 10) or np.any(self.grad_rho_mask > 10):
            raise ValueError('Inversion: the mask of the model parameters is greater than 10, too large.')

        # check the method: SD, CG, LBFGS, PLBFGS, TRN, PTRN
        if self.method not in ['SD', 'CG', 'LBFGS', 'PLBFGS', 'TRN', 'PTRN']:
            raise ValueError(f'Inversion: the method {self.method} is not supported.')

        # # check the filter
        # if self.filter is not None:
        #     if len(self.filter) != 4 or \
        #         not 0.0 < self.filter[0] < self.filter[1] < self.filter[2] < self.filter[3]:
        #         raise ValueError(f'Inversion: the filter {self.filter} is not supported.')


        # print the parameters
        print('\n')
        print('****************************************************************')
        print('          IMAGEX: 2D Elastic Wave Full Waveform Inversion       ')
        print('****************************************************************')
        print('\nInversion:')
        print(f'    Model       : nx = {self.nx}, nz = {self.nz}, dx = {self.dx} m')
        print(f'    Waveform    : nt = {self.nt}, dt = {self.dt*1000:.2f} ms, t = 0 ~ {self.t[-1]:.2f} s')
        print(f'    Sources     : {len(self.ind_src_x)} shots, {self.f0} Hz Ricker wavelet')
        print(f'    Geophone pr : weight {self.weight_pr}, {len(self.ind_rec_x)} receivers')
        print(f'    Geophone vx : weight {self.weight_vx}, {len(self.ind_rec_x)} receivers')
        print(f'    Geophone vz : weight {self.weight_vz}, {len(self.ind_rec_x)} receivers')
        print(f'    DAS Strain  : weight {self.weight_et}, {len(self.ind_das_x)} channels')
        print(f'    Vp  Range   : {self.vp_int.min():7.2f} ~ {self.vp_int.max():7.2f} m/s')
        print(f'    Vs  Range   : {self.vs_int.min():7.2f} ~ {self.vs_int.max():7.2f} m/s')
        print(f'    Rho Range   : {self.rho_int.min():7.2f} ~ {self.rho_int.max():7.2f} kg/m^3')
        print(f'    Vp  Mask    : {self.grad_vp_mask.min():.2f} ~ {self.grad_vp_mask.max():.2f}')
        print(f'    Vs  Mask    : {self.grad_vs_mask.min():.2f} ~ {self.grad_vs_mask.max():.2f}')
        print(f'    Rho Mask    : {self.grad_rho_mask.min():.2f} ~ {self.grad_rho_mask.max():.2f}')
        print(f'    Method      : {self.method}')
        print(f'    MaxIter     : {self.niter_max}')
        print(f'    Conv        : {self.conv}')
        print(f'    GPU Cards   : {self.ngpu} GPU')
        print(f'    Data path   : {os.path.abspath(self.data_path)}')
        print(f'    Output path : {os.path.abspath(self.output_path)}')
        print('****************************************************************')
        print('\nInversion: start running...\n')



    def __set_default_inversion(self, save_scratch=False):
        ''' Set the problem to be optimized and the solver
        '''

        # Set the propagator
        propagator = ElasticPropagator(self.data_path, self.nx, self.nz, 
                                       self.dx, self.dz, self.nt, self.dt, 
                                       self.f0, self.stf, self.ind_src_x, 
                                       self.ind_src_z, self.ind_rec_x, 
                                       self.ind_rec_z, self.ind_das_x, 
                                       self.ind_das_z, self.das_wt_x, 
                                       self.das_wt_z, self.das_gl, 
                                       self.vp_int, self.vs_int, self.rho_int,
                                       self.weight_pr, self.weight_vx, 
                                       self.weight_vz, self.weight_et,
                                       npml=self.npml, 
                                       save_scratch=save_scratch)
        

        # Set the problem, elastic FWI problem without any regularization
        self.problem = ElasticProblem(propagator)

        # Set the initial model
        self.model_int = merge_model(self.vp_int, self.vs_int, self.rho_int)

        # Set bounds
        self.lb = merge_model(self.vp_lb, self.vs_lb, self.rho_lb)
        self.ub = merge_model(self.vp_ub, self.vs_ub, self.rho_ub)

        # Set the solver
        self.solver = Solver(niter_max=self.niter_max, conv=self.conv, 
                             method=self.method, bound=True, lb=self.lb, 
                             ub=self.ub, lbfgs_memory=5, debug=self.debug)


    def run(self, data_path=None, model_int=None, save_model=False, output_prefix='fwi', 
            save_scratch=False):
        ''' Run the inversion workflow
        '''

        # set timer
        start_time = time.time()

        # set the data path if required, it means a new problem is set
        if data_path is not None:
            self.__set_default_inversion()
            self.problem.propagator.set_data_path(data_path)
            print(f'Inversion: set the data path to {data_path}')
        
        if output_prefix != '':
            self.solver.suffix = output_prefix

        if save_scratch:
            self.__set_default_inversion(save_scratch=True)

        # set the initial model as the current model
        model = self.model_int.copy() if model_int is None else model_int.copy()

        # obatin the gradient of the initial model
        fcost, grad, grad_preco = self.problem.apply_gradient(
            model, self.grad_vp_mask, self.grad_vs_mask, self.grad_rho_mask, 
            ngpu=self.ngpu, first_iter=True)

        # save the initial model and gradient, if required
        if save_model:
            self.problem.save_model(model, grad, os.path.join(self.output_path, 
                    f'{output_prefix}_result_iter_{0:04d}'))

        # optimization loop
        while self.solver.FLAG != 'CONV' and self.solver.FLAG != 'FAIL':
            # update the model
            model = self.solver.iterate(model, fcost, grad, grad_preco)

            # save the model and gradient, if required
            if save_model:
                self.problem.save_model(model, grad, os.path.join(self.output_path, 
                        f'{output_prefix}_result_iter_{self.solver.cpt_iter+1:04d}'))

            if self.solver.FLAG == 'GRAD':

                # compute cost and gradient of the updated model
                fcost, grad, grad_preco = self.problem.apply_gradient(
                    model, self.grad_vp_mask, self.grad_vs_mask, 
                    self.grad_rho_mask, ngpu=self.ngpu)

        # save the final model and gradient
        self.problem.save_model(model, grad, os.path.join(self.output_path, f'{output_prefix}_result_final'))

        #  print the elapsed time
        print_time('Inversion', start_time, time.time())

        return model
 

if __name__ == '__main__':
    ''' Main program for inversion

    Usage: python inversion.py parfile
           python inversion.py parfile --verbose

    '''
    # Parse command line arguments

    parser = argparse.ArgumentParser(description='Perform inversion')
    parser.add_argument('parfile', type=str, nargs='+', help='Parameter file(s) with ".yaml" extension')

    # save the model and gradient, if required
    parser.add_argument('--save_model', action='store_true',
                        help='save the model and gradient, default is False')

    # save the scratch files, if required
    parser.add_argument('--save_scratch', action='store_true',
                        help='save the scratch files in inversion, default is False')

    parser.add_argument('--verbose', action='store_true',
                        help='verbose mode, default is False')

    args = parser.parse_args()


    # Loop through each parfile and call the main function
    for parfile in args.parfile:
        
        # Print the parfile
        print(f'Inversion: parfile = {parfile}')
        
        # Run Full-waveform inversion
        inversion = Inversion(parfile, args.verbose)

        _ = inversion.run(save_model=args.save_model, save_scratch=args.save_scratch)


