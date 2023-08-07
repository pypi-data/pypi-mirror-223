import numpy as np


# pick the first arrival of the signal

def brutal_picker(trace, threshold = 0.01):
    ''' pick the first arrival based on the amplitude of the trace 

    Parameters
    ----------
        trace: 2D array of float
            the seismic traces
        
        Returns
        -------
        pick: 1D array of int
            the index of the first arrival
    '''

    pick = [(abs(trace[i]) > threshold * np.max(abs(trace[i]))).argmax(axis=-1) 
        for i in range(len(trace))]

    return np.array(pick)