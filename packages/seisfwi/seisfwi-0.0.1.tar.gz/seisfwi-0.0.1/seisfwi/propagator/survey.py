import numpy as np
import os


class Survey(object):
    ''' Survey class describes the seismic acquisition geometry
    Parameters
    ----------
        :param str path: the path of the model
        :param int gpu_num: the number of GPU cards
        :param list of numpy.ndarray src_coord: the coordinates of the source
        :param list of numpy.ndarray src_wavelet: the wavelet of the source
        :param list of numpy.ndarray rec_coord: the coordinates of the receiver
        :param list of str rec_comp: the components of the receiver
    '''

    def __init__(self, path: str, gpu_num: int, src_coord: list,
                 src_wavelet: list, rec_coord: list, rec_comp: list, 
                 dt: float, nt: int):
        ''' Initialize the source parameters
        '''

        self.path = path
        self.gpu_num = gpu_num
        self.src_coord = src_coord
        self.src_wavelet = src_wavelet
        self.rec_coord = rec_coord
        self.rec_comp = rec_comp
        self.dt = dt
        self.nt = nt

        self.src_num = len(self.src_coord)
        self.rec_data = None

        # analyze the survey parameters
        self.analyze()


    def analyze(self):
        ''' Analyze the survey parameters
        '''

        # path
        if self.path[-1] != '/':
            self.path += '/'

        # check the existence of the working path
        if not os.path.exists(self.path):
            os.makedirs(self.path)

        # gpu device
        if self.gpu_num < 0:
            raise ValueError(
                'GPU Error: the number of GPU devices is negative.')

        # check coordinates of sources
        if self.src_coord.shape != (self.num, 2):
            raise ValueError(
                'Source Error: the source coordinates must be 2D array with dimensions of [src_num, 2]')

        # check the source wavelet
        if self.src_wavelet.shape[0] != self.num:
            raise ValueError(
                'Source Error: the number of source wavelets must be the same as the number of sources')
        
        for i in range(self.num):
            if self.src_wavelet[i].shape[0] != self.nt:
                raise ValueError(
                    'Source Error: the length of source wavelets must be the same as the number of time steps')

        # check the receiver coordinates
        if len(self.rec_coord) != self.num:
            raise ValueError(
                'Receiver Error: receiver coordinates must be a list of the length of the source number, with a 2D array for x and z coordinates')

        # check the receiver components
        if self.rec_comp.lower() not in ['vx', 'vz', 'p', 'das']:
            msg = 'Receiver Error: receiver component must be vx, vz or p'
            err = 'Unsupport receiver component: {}'.format(self.comp)
            raise ValueError(msg + '\n' + err)


    def analyzeModel(self, model):
        
        # get the model parameters
        v_max = np.max(model.vp)
        v_min = np.min(model.vs) if np.min(model.vs) > 0 else np.min(model.vp)
        dx = model.dx
        dz = model.dz
        dh = np.min([dx, dz])
        x = model.x
        z = model.z
        
        dt = self.dt
        f0 = self.f0

        # check the Courant number for stability condition
        Courant_number = v_max * dt * np.sqrt(2.0) * (1.0 / 24.0 + 9.0 / 8.0) / dh
        if Courant_number > 1.0:
            raise RuntimeError('The Courant number is larger than 1.0!')

        # check the numerical dispersion condition
        dx0 = v_min / f0 / 10.
        f00 = v_min / dh / 10.

        if dx0 < dx:
            print('Survey Warning: numerical dispersion, dx = {:6.2f} m  > dx_required = {:6.2f} m'.format(dx, dx0))
            print('Survey Warning: numerical dispersion, f0 = {:6.2f} Hz > f0_required = {:6.2f} Hz'.format(f0, f00))
  
        # check the source location is inside the model
        if (self.source.coord[:,0].min() < x.min() or 
            self.source.coord[:,0].max() > x.max() or
            self.source.coord[:,1].min() < z.min() or 
            self.source.coord[:,1].max() > z.max()):
            raise ValueError('Survey Error: source location is out of model range')

        # check the receiver location is inside the model
        for rec in self.rec_coord:
            if (rec[:, 0].min() < x.min() or 
                rec[:, 0].max() > x.max() or
                rec[:, 1].min() < z.min() or 
                rec[:, 1].max() > z.max()):
                raise ValueError('Survey Error: receiver location is out of model range')
        

    #TODO: rewrite the __add__ function for combining two surveys, I need to 
    # deal with different types of receivers
    # def __add__(self, other_survey):

    #     # check the type of the other survey
    #     if not isinstance(other_survey, Survey):
    #         raise TypeError(
    #             'Survey Error: the other survey must be an instance of Survey')
 
