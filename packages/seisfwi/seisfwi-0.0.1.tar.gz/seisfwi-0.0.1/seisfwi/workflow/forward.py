#!/usr/bin/env python3

import argparse
import numpy as np
import os
import time

from imagex.propagator import ElasticPropagator
from imagex.utils import check_shape, load_yaml, print_time


class Forward(object):
    ''' Forward modeling class
    '''

    def __init__(self, parfile, verbose=False):
        ''' Initialize the forward modeling class
        '''

        # load parameters
        params = load_yaml(parfile)

        # checkl and load the model
        self.__load_params(params, verbose)


    def __load_params(self, params, verbose):
        ''' Load the parameters, including the model, source and receiver
        '''

        # convert the dictionary to object attributes
        for _, value in params.items():
            for k, v in value.items():
                setattr(self, k, v)

        # set the parameters list for checking
        para_list = ['path', 'nx', 'nz', 'dx', 'dz', 'das_gl', 'nt', 'dt', 'f0',
                     'npml', 'ngpu', 'ind_src_file', 'stf_file', 'ind_rec_file', 'ind_das_file', 
                     'das_wt_file', 'vp_file', 'vs_file', 'rho_file']

        if not hasattr(self, 'npml'):
            self.npml = 20

        if not hasattr(self, 'ngpu'):
            self.ngpu = 1

        # check the existence of the parameters
        for para in para_list:
            if not hasattr(self, para):
                raise ValueError(f'Forward: parameter {para} is missing!')

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

        # check the shape
        for data in [ind_src, ind_rec, ind_das, das_wt]:
            if data.shape[0] != 2:
                raise ValueError(
                    f'the shape of source/receiver/DAS/weight file is not correct!')

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

        # set the default receiver weight for all components in forward modeling
        self.weight_pr = 1.0
        self.weight_vx = 1.0
        self.weight_vz = 1.0
        self.weight_et = 1.0

        # load the model
        for par in ['vp', 'vs', 'rho']:
            data = np.load(getattr(self, par + '_file'))
            check_shape(data, (self.nz, self.nx))
            setattr(self, par, data)

        # print the parameters
        print('\n')
        print('****************************************************************')
        print('          IMAGEX: 2D Elastic Wave Forward Modeling              ')
        print('****************************************************************')
        print('\nForward:')
        print(f'    Model       : nx = {self.nx}, nz = {self.nz}, dx = {self.dx} m')
        print(f'    Waveform    : nt = {self.nt}, dt = {self.dt*1000:.2f} ms, t = 0 ~ {self.t[-1]:.2f} s')
        print(f'    Sources     : {len(self.ind_src_x)} shots, {self.f0} Hz Ricker wavelet')
        print(f'    Geophone    : {len(self.ind_rec_x)} receivers')
        print(f'    DAS         : {len(self.ind_das_x)} channels')
        print(f'    Vp  Range   : {self.vp.min():7.2f} ~ {self.vp.max():7.2f} m/s')
        print(f'    Vs  Range   : {self.vs.min():7.2f} ~ {self.vs.max():7.2f} m/s')
        print(f'    Rho Range   : {self.rho.min():7.2f} ~ {self.rho.max():7.2f} kg/m^3')
        print(f'    GPU Cards   : {self.ngpu} GPU')
        print(f'    Output path : {os.path.abspath(self.path)}')
        print('****************************************************************')


    def run(self):
        ''' Run the forward modeling
        '''

        # Set the start time
        start_time = time.time()

        # Set the propagator
        self.propagator = ElasticPropagator(self.path, self.nx, self.nz, 
                                            self.dx, self.dz, self.nt, self.dt, 
                                            self.f0, self.stf, self.ind_src_x, 
                                            self.ind_src_z, self.ind_rec_x,
                                            self.ind_rec_z, self.ind_das_x, 
                                            self.ind_das_z, self.das_wt_x, 
                                            self.das_wt_z, self.das_gl,
                                            self.vp, self.vs, self.rho,
                                            self.weight_pr, self.weight_vx,
                                            self.weight_vz, self.weight_et,
                                            npml=self.npml)

        print('\nForward modeling: start running...\n')

        # Launch the forward modeling
        self.propagator.apply_forward(ngpu=self.ngpu)

        #  Print the elapsed time
        print_time('Forward modeling', start_time, time.time())


if __name__ == '__main__':
    ''' Main program for forward modeling

    Usage: python forward.py parfile
           python forward.py parfile --verbose

    '''

    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Perform forward modeling')
    
    # Add arguments for parameter file, if multiple parameter files are needed, perform forward modeling multiple times
    parser.add_argument('parfile', type=str, nargs='+', help='Parameter file(s) with ".yaml" extension')
    parser.add_argument('--verbose', action='store_true',help='verbose mode, default is False')

    # Parse the arguments
    args = parser.parse_args()

    # Loop through each parfile and call the main function
    for parfile in args.parfile:
        if not parfile.lower().endswith('.yaml'):
            raise ValueError(f"Error: Invalid parfile format for '{parfile}'. It should end with '.yaml'")

        # print the parameter file
        print(f"Forward modeling with parameter file: {parfile}")

        # Run forward modeling
        forward = Forward(parfile, args.verbose)

        forward.run()
