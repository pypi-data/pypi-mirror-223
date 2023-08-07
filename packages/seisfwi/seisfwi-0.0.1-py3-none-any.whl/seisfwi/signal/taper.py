import numpy as np


def taper(stf, n=20):
    ''' taper the source time function
    '''

    stf[0:n] = 0
    stf[n:2*n] = np.sin(np.pi/2*np.arange(0, n)/n) * stf[n:2*n]

    return stf
