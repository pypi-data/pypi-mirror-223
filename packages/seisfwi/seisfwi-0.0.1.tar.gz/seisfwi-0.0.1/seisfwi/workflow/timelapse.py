#!/usr/bin/env python3

import argparse
import numpy as np
import os
import time
import copy

from imagex.solver import Solver
from imagex.utils.tools import print_time, calculate_double_difference, merge_model, split_model
from imagex.workflow.inversion import Inversion
from imagex.problem import SimuElasticProblem


class TimelapseInversion(Inversion):
    ''' Timelapse inversion class by inheriting from Inversion class.
        Add more functions to perform timelapse inversion.
        Rewrite the run() function to perform timelapse inversion.
    '''


    def __init__(self, parfile, verbose=False):
        ''' Initialize the TimelapseInversion class
        '''

        # initialize the Inversion class
        super().__init__(parfile, verbose=verbose)

        # check the parameters specific to timelapse inversion and data files
        self.__check_timelapse(verbose=verbose)



    def __check_timelapse(self, verbose):
        ''' Check the existence of the parameters, for timelapse inversion
        '''

        # check the baseline data path. Set it to the data_path if not specified
        if not hasattr(self, 'data_bl'):
            self.data_bl = self.data_path

        # check the monitor data path
        if not hasattr(self, 'data_ml'):
            raise ValueError('Parameter data_ml is missing!')

        if not hasattr(self, 'tl_method'):
            raise ValueError('Parameter tl_method is missing!')
        elif self.tl_method not in methods:
            raise ValueError(f'Parameter tl_method is not supported! Available methods are {methods}')


        # check the data files
        self.inv_comp = []

        if self.weight_pr > 0:
            self.inv_comp.append('pr')
        if self.weight_vx > 0:
            self.inv_comp.append('vx')
        if self.weight_vz > 0:
            self.inv_comp.append('vz')
        if self.weight_et > 0:
            self.inv_comp.append('et')

        nsrc = len(self.ind_src_x)
        for isrc in range(nsrc):
            for comp in self.inv_comp:
                file_bl = os.path.join(self.data_bl, f'shot{isrc}_{comp}.bin')
                file_ml = os.path.join(self.data_ml, f'shot{isrc}_{comp}.bin')
                if not os.path.exists(file_bl):
                    raise ValueError(f'Inversion: the baseline data file {file_bl} does not exist.')
                if not os.path.exists(file_ml):
                    raise ValueError(f'Inversion: the monitor data file {file_ml} does not exist.')



    def parallel_inversion(self, save_model=False):
        ''' Perform parallel inversion
        '''
        # set the initial model
        model_int = merge_model(self.vp_int, self.vs_int, self.rho_int)

        # run 1: Initial model -- baseline data -->  baseline model
        model_bl = self.run(data_path=self.data_bl, model_int=model_int, save_model=save_model, output_prefix='bl')

        # run 2: Initial model -- monitor data  -->  monitor model
        model_ml = self.run(data_path=self.data_ml, model_int=model_int, save_model=save_model, output_prefix='ml')

        # split the model into vp, vs, rho
        vp_bl, vs_bl, rho_bl = split_model(model_bl, self.nx, self.nz)
        vp_ml, vs_ml, rho_ml = split_model(model_ml, self.nx, self.nz)

        # time-lapse changes
        vp_tl, vs_tl, rho_tl = vp_ml - vp_bl, vs_ml - vs_bl, rho_ml - rho_bl

        # put all results into a dictionary
        result = {'vp_bl': vp_bl, 'vs_bl': vs_bl, 'rho_bl': rho_bl,
                  'vp_ml': vp_ml, 'vs_ml': vs_ml, 'rho_ml': rho_ml,
                  'vp_tl': vp_tl, 'vs_tl': vs_tl, 'rho_tl': rho_tl}
   
        return result



    def sequential_inversion(self, save_model=False):
        ''' Perform sequential inversion
        '''

        # set the initial model
        model_int = merge_model(self.vp_int, self.vs_int, self.rho_int)

        # run 1: Initial model -- baseline data -->  baseline model
        model_bl = self.run(data_path=self.data_bl, model_int=model_int, save_model=save_model, output_prefix='bl')

        # run 2: baseline model -- monitor data  -->  monitor model
        model_ml = self.run(data_path=self.data_ml, model_int=model_bl, save_model=save_model, output_prefix='ml')

        # split the model into vp, vs, rho
        vp_bl, vs_bl, rho_bl = split_model(model_bl, self.nx, self.nz)
        vp_ml, vs_ml, rho_ml = split_model(model_ml, self.nx, self.nz)

        # time-lapse changes
        vp_tl, vs_tl, rho_tl = vp_ml - vp_bl, vs_ml - vs_bl, rho_ml - rho_bl

        # put all results into a dictionary
        result = {'vp_bl': vp_bl, 'vs_bl': vs_bl, 'rho_bl': rho_bl,
                  'vp_ml': vp_ml, 'vs_ml': vs_ml, 'rho_ml': rho_ml,
                  'vp_tl': vp_tl, 'vs_tl': vs_tl, 'rho_tl': rho_tl}

        return result
    

    def center_difference_inversion(self, save_model=False):
        ''' Perform center difference inversion
        '''

        # set the initial model
        model_int = merge_model(self.vp_int, self.vs_int, self.rho_int)

        # run 1: Initial model -- baseline data -->  baseline1 model
        model_bl1 = self.run(data_path=self.data_bl, model_int=model_int, save_model=save_model, output_prefix='bl1')

        # run 2: baseline1 model -- monitor data  -->  monitor1 model
        model_ml1 = self.run(data_path=self.data_ml, model_int=model_bl1, save_model=save_model, output_prefix='ml1')
      
        # run 3: Initial model -- monitor data  -->  monitor2 model
        model_ml2 = self.run(data_path=self.data_ml, model_int=model_int, save_model=save_model, output_prefix='ml2')

        # run 4: monitor2 model -- baseline data -->  baseline2 model        
        model_bl2 = self.run(data_path=self.data_bl, model_int=model_ml2, save_model=save_model, output_prefix='bl2')
        
        # split the model into vp, vs, rho
        vp_bl1, vs_bl1, rho_bl1 = split_model(model_bl1, self.nx, self.nz)
        vp_bl2, vs_bl2, rho_bl2 = split_model(model_bl2, self.nx, self.nz)
        vp_ml1, vs_ml1, rho_ml1 = split_model(model_ml1, self.nx, self.nz)
        vp_ml2, vs_ml2, rho_ml2 = split_model(model_ml2, self.nx, self.nz)
    
        # time-lapse changes
        vp_tl = ((vp_ml1 - vp_bl1) + (vp_ml2 - vp_bl2)) / 2.0
        vs_tl = ((vs_ml1 - vs_bl1) + (vs_ml2 - vs_bl2)) / 2.0
        rho_tl = ((rho_ml1 - rho_bl1) + (rho_ml2 - rho_bl2)) / 2.0
    
        # put all results into a dictionary
        result = {'vp_bl1': vp_bl1, 'vs_bl1': vs_bl1, 'rho_bl1': rho_bl1,
                  'vp_bl2': vp_bl2, 'vs_bl2': vs_bl2, 'rho_bl2': rho_bl2,
                  'vp_ml1': vp_ml1, 'vs_ml1': vs_ml1, 'rho_ml1': rho_ml1,
                  'vp_ml2': vp_ml2, 'vs_ml2': vs_ml2, 'rho_ml2': rho_ml2,
                  'vp_tl' : vp_tl,  'vs_tl' : vs_tl,  'rho_tl' : rho_tl}

        return result



    def cross_update_inversion(self, save_model=False):
        ''' Perform cross update inversion
        '''

        # set the initial model
        model_int = merge_model(self.vp_int, self.vs_int, self.rho_int)

        # run 1: Initial model -- baseline data -->  baseline1 model
        model_bl1 = self.run(data_path=self.data_bl, model_int=model_int, save_model=save_model, output_prefix='bl1')

        # run 2: baseline1 model -- monitor data  -->  monitor1 model
        model_ml1 = self.run(data_path=self.data_ml, model_int=model_bl1, save_model=save_model, output_prefix='ml1')

        # run 3: monitor1 model -- baseline data  -->  baseline2 model
        model_bl2 = self.run(data_path=self.data_bl, model_int=model_ml1, save_model=save_model, output_prefix='bl2')

        # run 4: baseline2 model -- monitor data  -->  monitor2 model
        model_ml2 = self.run(data_path=self.data_ml, model_int=model_bl2, save_model=save_model, output_prefix='ml2')
    
        # split the model into vp, vs, rho
        vp_bl1, vs_bl1, rho_bl1 = split_model(model_bl1, self.nx, self.nz)
        vp_bl2, vs_bl2, rho_bl2 = split_model(model_bl2, self.nx, self.nz)
        vp_ml1, vs_ml1, rho_ml1 = split_model(model_ml1, self.nx, self.nz)
        vp_ml2, vs_ml2, rho_ml2 = split_model(model_ml2, self.nx, self.nz)

        # time-lapse changes
        vp_tl, vs_tl, rho_tl = (vp_ml2 - vp_bl2), (vs_ml2 - vs_bl2), (rho_ml2 - rho_bl2)

        # put all results into a dictionary
        result = {'vp_bl1': vp_bl1, 'vs_bl1': vs_bl1, 'rho_bl1': rho_bl1,
                  'vp_bl2': vp_bl2, 'vs_bl2': vs_bl2, 'rho_bl2': rho_bl2,
                  'vp_ml1': vp_ml1, 'vs_ml1': vs_ml1, 'rho_ml1': rho_ml1,
                  'vp_ml2': vp_ml2, 'vs_ml2': vs_ml2, 'rho_ml2': rho_ml2,
                  'vp_tl' : vp_tl,  'vs_tl' : vs_tl,  'rho_tl' : rho_tl}
        
        return result


    def double_difference_inversion(self, save_model=False):
        '''
        '''

        # set the initial model
        model_int = merge_model(self.vp_int, self.vs_int, self.rho_int)

        # run 1: Initial model -- baseline data -->  baseline model
        model_bl = self.run(data_path=self.data_bl, model_int=model_int, save_model=save_model, output_prefix='bl')

        # prepare the double-difference data
        data_path_dd = os.path.join(os.path.dirname(self.data_bl), 'data_dif')

        # Set the propagator
        self.problem.propagator.set_data_path(data_path_dd)

        # compute the baseline data
        vp_bl, vs_bl, rho_bl = split_model(model_bl, self.nx, self.nz)
        self.problem.propagator.apply_forward(vp = vp_bl, vs = vs_bl, 
                                              rho = rho_bl, ngpu = self.ngpu)

        # compute the double-difference data
        for isrc in range(len(self.ind_src_x)):
            for comp in self.inv_comp:
                obs_bl = os.path.join(self.data_bl, f'shot{isrc}_{comp}.bin')
                obs_ml = os.path.join(self.data_ml, f'shot{isrc}_{comp}.bin')
                syn_bl = os.path.join(data_path_dd, f'shot{isrc}_{comp}.bin')
                calculate_double_difference(obs_ml, obs_bl, syn_bl)

        # run 2: baseline model -- double-difference data -->  monitor model
        model_ml = self.run(data_path=data_path_dd, model_int=model_bl, save_model=save_model, output_prefix='ml')

        # split the model into vp, vs, rho
        vp_ml, vs_ml, rho_ml = split_model(model_ml, self.nx, self.nz)

        # time-lapse changes
        vp_tl, vs_tl, rho_tl = (vp_ml - vp_bl), (vs_ml - vs_bl), (rho_ml - rho_bl)

        # put all results into a dictionary
        result = {'vp_bl': vp_bl, 'vs_bl': vs_bl, 'rho_bl': rho_bl,
                  'vp_ml': vp_ml, 'vs_ml': vs_ml, 'rho_ml': rho_ml,
                  'vp_tl': vp_tl, 'vs_tl': vs_tl, 'rho_tl': rho_tl}
        
        return result


    def simultaneous_inversion(self, save_model=False):
        ''' Perform simultaneous inversion
        '''

        # set the scaling factors
        alpha = 1.0    # weight for the baseline data
        beta  = 1.0    # weight for the monitor data

        # # set the initial model
        # model_int = merge_model(self.vp_int, self.vs_int, self.rho_int)

        # # run 1: Initial model -- baseline data -->  baseline model
        # model_bl = self.run(data_path=self.data_bl, model_int=model_int, save_model=save_model, output_prefix='bl')

        # run 2: Baseline model -- baseline & monitor data  -->  baseline & monitor model
        problem_bl = copy.deepcopy(self.problem)
        problem_ml = copy.deepcopy(self.problem)

        # Set the propagator
        problem_bl.propagator.set_data_path(self.data_bl)
        problem_ml.propagator.set_data_path(self.data_ml)

        # Set the problem
        self.problem = SimuElasticProblem(problem_bl, problem_ml, alpha, beta)

        # Set the initial model
        model_int = np.concatenate((self.vp_int.flatten(), self.vs_int.flatten(), self.rho_int.flatten()))
        self.model_int = np.concatenate((model_int, model_int))
        # self.model_int = np.concatenate((model_bl, model_bl))

        # Set bounds
        lb = np.concatenate((self.vp_lb.flatten(), self.vs_lb.flatten(), self.rho_lb.flatten()))
        ub = np.concatenate((self.vp_ub.flatten(), self.vs_ub.flatten(), self.rho_ub.flatten()))
        self.lb = np.concatenate((lb, lb))
        self.ub = np.concatenate((ub, ub))

        # Set the solver
        self.solver = Solver(niter_max=self.niter_max, conv=self.conv, method=self.method, 
                             bound=True, lb=self.lb, ub=self.ub, lbfgs_memory=5, 
                             debug=self.debug)

        # Run the inversion, never provide the path
        model_all = self.run(save_model=save_model, output_prefix='simu')

        # split the model into vp, vs, rho
        vp_bl, vs_bl, rho_bl = split_model(model_all[:self.nx*self.nz * 3], self.nx, self.nz)
        vp_ml, vs_ml, rho_ml = split_model(model_all[self.nx*self.nz * 3:], self.nx, self.nz)

        # time-lapse changes
        vp_tl, vs_tl, rho_tl = (vp_ml - vp_bl), (vs_ml - vs_bl), (rho_ml - rho_bl)

        # put all results into a dictionary
        result = {'vp_bl': vp_bl, 'vs_bl': vs_bl, 'rho_bl': rho_bl,
                  'vp_ml': vp_ml, 'vs_ml': vs_ml, 'rho_ml': rho_ml,
                  'vp_tl': vp_tl, 'vs_tl': vs_tl, 'rho_tl': rho_tl}
        
        return result


    def workflow(self, save_model=False):
        ''' Run the timelapse inversion
        '''

        start_time = time.time()

        if self.tl_method == 'parallel':
            result = self.parallel_inversion(save_model=save_model)

        elif self.tl_method == 'sequential':
            result = self.sequential_inversion(save_model=save_model)

        elif self.tl_method == 'cross-update':
            result = self.cross_update_inversion(save_model=save_model)

        elif self.tl_method == 'center-difference':
            result = self.center_difference_inversion(save_model=save_model)

        elif self.tl_method == 'double-difference':
            result = self.double_difference_inversion(save_model=save_model)

        elif self.tl_method == 'simultaneous':
            result = self.simultaneous_inversion(save_model=save_model)

        else:
            raise ValueError(
                f'Inversion Error: the method {self.tl_method} is not supported! Available methods are {self.tl_method}')

        # save  the results
        filename = os.path.join(self.output_path, f'result_final_{self.tl_method}.npz')
        np.savez(filename, **result)
        print(f'See the results in {filename}\n')

        # print the elapsed time
        print_time('Time-lapse Inversion', start_time, time.time())



methods  = ['parallel', 'sequential', 'double-difference', 
            'simultaneous', 'center-difference', 'cross-update']

if __name__ == '__main__':

    # parse the command-line arguments
    parser = argparse.ArgumentParser(description='Timelapse inversion')
    parser.add_argument('parfile', type=str, nargs='+', help='Parameter file(s) with ".yaml" extension')

    # save the model and gradient, if required
    parser.add_argument('--save_model', action='store_true', help='save the model and gradient, default is False')
    parser.add_argument('--verbose', action='store_true', help='verbose mode')

    # parse the arguments
    args = parser.parse_args()

    # Loop through each parfile and call the main function
    for parfile in args.parfile:

        # check the parfile
        if not parfile.lower().endswith('.yaml'):
            raise ValueError(f"Error: Invalid parfile format for '{parfile}'. It should end with '.yaml'")

        # print the parameter file
        print(f"Time-lapse inversion with parameter file: {parfile}")

        # initialize the TimelapseInversion class
        timelapse = TimelapseInversion(parfile, verbose=args.verbose)

        # run the timelapse inversion
        timelapse.workflow(save_model=args.save_model)
