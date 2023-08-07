import os
import torch
import numpy as np

from torch.utils.cpp_extension import load

from imagex.utils import check_shape, save_json
from imagex.propagator.utils import (check_stability, check_dispersion, check_index_range, pad_array)


class ElasticPropagator(object):
    ''' The class of defining the propagator for the isotropic elastic wave 
        equation (stress-velocity form), which is solved by the finite 
        difference method.
    '''

    def __init__(self, path, nx, nz, dx, dz, nt, dt, f0, stf, ind_src_x, ind_src_z, 
                 ind_rec_x, ind_rec_z, ind_das_x, ind_das_z, das_wt_x, das_wt_z, 
                 das_gl, vp, vs, rho, weight_pr, weight_vx, weight_vz, weight_et, 
                 npml=20, save_scratch=False):
        
        ''' Initialize the propagator

        Parameters:
        -----------
        :param int nx: number of grid points in x-direction
        :param int nz: number of grid points in z-direction
        :param float dx: grid spacing in x-direction
        :param float dz: grid spacing in z-direction
        :param int nt: number of time steps
        :param float dt: time step size
        :param float f0: dominant frequency of the source wavelet
        :param np.array stf: source wavelet
        :param np.array ind_src_x: x-indices of source locations
        :param np.array ind_src_z: z-indices of source locations
        :param np.array ind_rec_x: x-indices of receiver locations
        :param np.array ind_rec_z: z-indices of receiver locations
        :param np.array ind_das_x: x-indices of DAS locations (No. channels + 1)
        :param np.array ind_das_z: z-indices of DAS locations (No. channels + 1)
        :param float gl: gauge length of DAS 
        :param float das_wt: weight of DAS, x component
        :param np.array vp: P-wave velocity model
        :param np.array vs: S-wave velocity model
        :param np.array rho: density model
        :param str path: path to the experiment directory
        :param float weight_pr: weight of pressure for inversion only
        :param float weight_vx: weight of vx for inversion only
        :param float weight_vz: weight of vz for inversion only
        :param float weight_et: weight of DAS strain rate for inversion only
        :param int npml: number of PML layers
        :param bool save_scratch: save the scratch files or not
        '''

        # set the parameters
        self.path = path
        self.nx = nx
        self.nz = nz
        self.dx = dx
        self.dz = dz
        self.nt = nt
        self.dt = dt
        self.f0 = f0
        self.stf = stf
        self.ind_src_x = ind_src_x
        self.ind_src_z = ind_src_z
        self.ind_rec_x = ind_rec_x
        self.ind_rec_z = ind_rec_z
        self.ind_das_x = ind_das_x
        self.ind_das_z = ind_das_z
        self.das_wt_x = das_wt_x
        self.das_wt_z = das_wt_z
        self.das_gl = das_gl
        self.vp = vp
        self.vs = vs
        self.rho = rho
        self.weight_pr = weight_pr
        self.weight_vx = weight_vx
        self.weight_vz = weight_vz
        self.weight_et = weight_et
        self.npml = npml
        self.save_scratch = save_scratch

        # set derived parameters
        npad = int(32 - np.mod((nz+2*npml), 32))
        self.npad = npad
        self.nz_pad = nz + 2*npml + npad
        self.nx_pad = nx + 2*npml
 
        # set source wavelet
        rec_num = len(ind_rec_x)
        src_num = len(ind_src_x)

        self.th_stf = torch.tensor(stf, dtype=torch.float32, requires_grad=False).repeat(src_num, 1)
        self.shot_ids = torch.tensor(np.arange(0, src_num), dtype=torch.int32)

        # analyze the geometry
        self.analyze_geometry()

        # set up path
        self.set_data_path(path)


    def analyze_geometry(self):
        ''' Analyze the geometry of the source and receivers
        '''
        
        # check the source location is inside the model
        check_index_range(self.ind_src_x, self.ind_src_z, self.nx, self.nz, tag = 'source')
        
        # check the receiver location is inside the model
        check_index_range(self.ind_rec_x, self.ind_rec_z, self.nx, self.nz, tag = 'receiver')

        # check the DAS location is inside the model
        check_index_range(self.ind_das_x, self.ind_das_z, self.nx, self.nz, tag = 'DAS')

        # check the DAS weight is normalized (equal to 1)
        if np.any(self.das_wt_x**2 + self.das_wt_z**2 - 1.0 > 1e-6):
            raise ValueError('Forward Error: DAS weight is not normalized')

        # DAS locations
        if len(self.ind_das_x) == 1:
            raise ValueError("DAS locations should be more than one")

        # check any duplicate receivers
        if len(self.ind_rec_x) != len(set(self.ind_rec_x)) and len(self.ind_rec_z) != len(set(self.ind_rec_z)):
            print('There are duplicate geophones. If it is not intended, please check the geophone locations!')

        # check any duplicate DAS, only throw warning
        if len(self.ind_das_x) != len(set(self.ind_das_x)) and len(self.ind_das_z) != len(set(self.ind_das_z)):
            print('There are duplicate DAS. If it is not intended, please check the DAS locations!')

        # check the weight is non-negative float
        if self.weight_pr < 0 or self.weight_vx < 0 or self.weight_vz < 0 or self.weight_et < 0:
            raise ValueError('Forward Error: weight should be non-negative')

        # check the length of source time function
        if len(self.stf) != self.nt:
            raise ValueError('Forward Error: length of source time function is not equal to nt')


    def set_data_path(self, path):
        ''' set the path of the source code
        '''

        # set up path
        self.data_dir_name = path
        self.para_fname = os.path.join(path, 'para_file.json')
        self.survey_fname = os.path.join(path, 'survey_file.json')
        if self.save_scratch:
            self.scratch_dir_name = os.path.join(os.path.dirname(path), 'scratch')
        else:
            self.scratch_dir_name = None

        if self.scratch_dir_name is not None:
            print("Warning: saving scratch files is very time consuming!")

        # prepare the parameter file
        self.prepare_para()

        # prepare the survey file
        self.prepare_survey()


    def prepare_para(self):
        ''' Prepare the parameter file for the forward simulation
        '''

        par_list = ['dz', 'dx', 'nt', 'dt', 'f0', 'npml', 'npad', 
                    'weight_pr', 'weight_vx', 'weight_vz', 'weight_et',]
        
        para = {}
        para['nz'] = self.nz_pad
        para['nx'] = self.nx_pad
        for par in par_list:
            para[par] = getattr(self, par)

        para['if_win'] = False
        para['if_src_update'] = False
        para['if_cross_misfit'] = False

        # The cuda file is not used as it is too slow.
        # The data and source wavelet is filtered in the python code.
        # if self.filter is not None:
            # para['filter'] = self.filter

        para['survey_fname'] = self.survey_fname
        para['data_dir_name'] = self.data_dir_name

        
        os.makedirs(self.data_dir_name, exist_ok=True)

        if (self.scratch_dir_name is not None):
            para['scratch_dir_name'] = self.scratch_dir_name
            os.makedirs(self.scratch_dir_name, exist_ok=True)

        # write the parameter file
        save_json(self.para_fname, para)


    def prepare_survey(self):
        ''' Prepare the survey file
        '''

        # TODO: different receivers for different shots
        nsrc = len(self.ind_src_x)
        nrec = len(self.ind_rec_x)
        ndas = len(self.ind_das_x)
        survey = {}
        survey['nShots'] = nsrc
        survey['gauge_length'] = self.das_gl

        for isrc in range(0, nsrc):
            shot = {}
            shot['z_src'] = self.ind_src_z[isrc].astype(int).tolist()
            shot['x_src'] = self.ind_src_x[isrc].astype(int).tolist()
            shot['nrec'] = nrec
            shot['z_rec'] = self.ind_rec_z.astype(int).tolist()
            shot['x_rec'] = self.ind_rec_x.astype(int).tolist()
            shot['ndas'] = ndas
            shot['z_das'] = self.ind_das_z.astype(int).tolist()
            shot['x_das'] = self.ind_das_x.astype(int).tolist()
            shot['das_wt_x'] = self.das_wt_x.tolist()
            shot['das_wt_z'] = self.das_wt_z.tolist()

            # if Windows != None:
            #     raise ValueError('Windows is not None, but not implemented yet.')
                # shot['win_start'] = Windows['shot' + str(i)][:start]
                # shot['win_end'] = Windows['shot' + str(i)][:end]

            survey['shot' + str(isrc)] = shot

        # save the survey file
        save_json(self.survey_fname, survey)


    def apply_forward(self, vp=None, vs=None, rho=None, ngpu=1):
        ''' Forward propagation
        '''

        # set the model parameters as torch tensors
        self.set_model(vp, vs, rho)

        # run the forward propagation code
        propagator.ElasticForward(self.th_lam_pad, self.th_mu_pad, self.th_rho_pad,
                                  self.th_stf, ngpu, self.shot_ids, self.para_fname)

    def apply_adjoint(self, vp=None, vs=None, rho=None, ngpu=1):
        ''' Adjoint propagation
        '''

        # set the model parameters as torch tensors
        self.set_model(vp, vs, rho)

        # run the forward propagation code
        propagator.ElasticAdjoint(self.th_lam_pad, self.th_mu_pad, self.th_rho_pad,
                                  self.th_stf, ngpu, self.shot_ids, self.para_fname)

    def apply_misfit(self, vp, vs, rho, ngpu=1):
        ''' Misfit calculation
        '''

        # set the model parameters as torch tensors
        self.set_model(vp, vs, rho)

        # run the forward propagation code
        outputs = propagator.ElasticMisfit(self.th_lam_pad, self.th_mu_pad,
                                           self.th_rho_pad, self.th_stf, ngpu,
                                           self.shot_ids, self.para_fname)

        return outputs[0].detach().cpu().numpy()[0]

    def apply_gradient(self, vp, vs, rho, ngpu=1):
        ''' Gradient calculation
        '''

        # set the model parameters as torch tensors
        self.set_model(vp, vs, rho)

        # run the forward propagation code
        outputs = propagator.ElasticGradient(self.th_lam_pad, self.th_mu_pad,
                                             self.th_rho_pad, self.th_stf, ngpu,
                                             self.shot_ids, self.para_fname)

        misfit = outputs[0].detach().cpu().numpy()
        misfit = misfit[0]
        grad_lam = outputs[1].detach().cpu().numpy()
        grad_mu = outputs[2].detach().cpu().numpy()
        grad_rho0 = outputs[3].detach().cpu().numpy()
        grad_stf = outputs[4].detach().cpu().numpy()

        # remove the padding
        npml = self.npml
        npad = self.npad
        grad_lam = grad_lam[npml:-(npad+npml), npml:-npml]
        grad_mu = grad_mu[npml:-(npad+npml), npml:-npml]
        grad_rho0 = grad_rho0[npml:-(npad+npml), npml:-npml]

        # compute the gradient with respect to vp, vs, and rho
        grad_vp = 2 * rho * vp * grad_lam
        grad_vs = -4 * rho * vs * grad_lam + 2 * rho * vs * grad_mu
        grad_rho = (vp**2 - 2 * vs**2) * grad_lam + \
            vs ** 2 * grad_mu + grad_rho0

        return misfit, grad_vp, grad_vs, grad_rho, grad_stf


    def set_model(self, vp = None, vs = None, rho = None):
        ''' Set the model parameters and check the stability condition and 
            numerical dispersion condition.
        '''

        # set the model parameters
        vp = self.vp if vp is None else vp
        vs = self.vs if vs is None else vs
        rho = self.rho if rho is None else rho

        # check the shape
        check_shape(vp, (self.nz, self.nx))
        check_shape(vs, (self.nz, self.nx))
        check_shape(rho, (self.nz, self.nx))

        # convert to lambda, mu, rho
        lam = rho * (vp**2 - 2 * vs**2)
        mu = rho * vs**2
        rho = rho

        # check if there is any negative lambda
        if (lam < 0).any():
            raise RuntimeError('There is negative lambda in the model!')

        # check the stability condition
        check_stability(vp, self.dt, self.dx)

        # check numerical dispersion condition
        check_dispersion(vp, vs, self.dx, self.f0)

        # pad the material parameters and convert to torch tensor
        lam_pad = pad_array(lam, self.npml, self.npad)
        mu_pad = pad_array(mu, self.npml, self.npad)
        rho_pad = pad_array(rho, self.npml, self.npad)

        # set the model parameters as torch tensor
        self.th_lam_pad = torch.tensor(lam_pad, dtype=torch.float32, requires_grad=False)
        self.th_mu_pad = torch.tensor(mu_pad,  dtype=torch.float32, requires_grad=False)
        self.th_rho_pad = torch.tensor(rho_pad, dtype=torch.float32, requires_grad=False)



def load_propagator(path):
    propagator = load(name="fwi",
                      sources=[path+'/libAPP.cpp',
                               path+'/Parameter.cpp',
                               path+'/IsoOperator.cu',
                               path+'/IsoElasticKernel.cu',
                               path+'/IsoAcousticKernel.cu',
                               path+'/Model.cu',
                               path+'/Cpml.cu',
                               path+'/utils.cu',
                               path+'/Survey.cu',
                               path+'/Boundary.cu'],

                      extra_cflags=['-O3 -fopenmp -lpthread'],
                      extra_include_paths=[
                          '/usr/local/cuda/include', path+'/rapidjson'],
                      extra_ldflags=[
                          '-L/usr/local/cuda/lib64 -lnvrtc -lcuda -lcudart -lcufft'],
                      build_directory=path+'/build/',
                      verbose=True)
    return propagator


# path of the source code and the build directory
abs_path = os.path.dirname(os.path.abspath(__file__))
path = os.path.join(abs_path, 'src')
os.makedirs(path+'/build/', exist_ok=True)

propagator = load_propagator(path)
