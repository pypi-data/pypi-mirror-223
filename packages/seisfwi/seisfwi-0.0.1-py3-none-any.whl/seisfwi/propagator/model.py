import numpy as np
from scipy.ndimage import gaussian_filter


class ElasticModel(object):
    ''' The class of defining the model parameters
    '''

    def __init__(self, nx: int, nz: int, dx: float, dz: float,
                 vp: np.ndarray, vs: np.ndarray, rho: np.ndarray,
                 npml: int = 20):
        ''' Initialize the model parameters
        '''

        # get the model parameters
        self.nx = nx
        self.nz = nz
        self.dx = dx
        self.dz = dz
        self.vp = vp
        self.vs = vs
        self.rho = rho
        self.npml = npml

        self.x = np.arange(0, self.nx) * self.dx + 0.0
        self.z = np.arange(0, self.nz) * self.dz + 0.0

        # analyze the model parameters
        self.analyze()

    def analyze(self):

        if self.nx <= 0 or self.nz <= 0:
            raise ValueError(
                'Model Error: the model size must be positive.')

        if self.dx <= 0 or self.dz <= 0:
            raise ValueError(
                'Model Error: the model interval must be positive.')

        if self.npml < 0:
            raise ValueError(
                'Model Error: the number of PML layers must be positive.')

        if self.vp.shape != (self.nx, self.nz):
            raise ValueError(
                'Model Error: the dimension of vp must be [nx, nz].')

        if self.vs.shape != (self.nx, self.nz):
            raise ValueError(
                'Model Error: the dimension of vs must be [nx, nz].')

        if self.rho.shape != (self.nx, self.nz):
            raise ValueError(
                'Model Error: the dimension of rho must be [nx, nz].')

    # def vpvsrho_lambdamu(self):
    #     ''' Calculate the lambda and mu parameters
    #     '''

    #     self.lam = self.rho * (self.vp ** 2 - 2 * self.vs ** 2)
    #     self.mu = self.rho * self.vs ** 2

    # def lambdamu_vpvsrho(self):
    #     ''' Calculate the vp and vs parameters
    #     '''
    #     self.vp = np.sqrt((self.lam + 2 * self.mu) / self.rho)
    #     self.vs = np.sqrt(self.mu / self.rho)

    def smooth(self, sigma: int = 10, water_layer: int = 0, parameter: str = 'all'):
        ''' Smooth the model parameters
        '''

        # check the parameter
        if parameter not in ['all', 'vp', 'vs', 'rho']:
            raise ValueError(
                'Model Error: the parameter must be one of vp, vs, rho, all.')

        # smooth the model parameters
        if parameter in ['all', 'vp']:
            if water_layer > 0:
                self.vp[:, water_layer:] = gaussian_filter(
                    self.vp[:,  water_layer:], sigma=sigma)
            else:
                self.vp = gaussian_filter(self.vp, sigma=sigma)

        if parameter in ['all', 'vs']:
            if water_layer > 0:
                self.vs[:,  water_layer:] = gaussian_filter(
                    self.vs[:,  water_layer:], sigma=sigma)
            else:
                self.vs = gaussian_filter(self.vs, sigma=sigma)

        if parameter in ['all', 'rho']:
            if water_layer > 0:
                self.rho[:,  water_layer:] = gaussian_filter(
                    self.rho[:,  water_layer:], sigma=sigma)
            else:
                self.rho = gaussian_filter(self.rho, sigma=sigma)

    def clone(self):
        ''' Clone the model
        '''

        return ElasticModel(self.nx, self.nz, self.dx, self.dz,
                            self.vp, self.vs, self.rho, self.npml)
