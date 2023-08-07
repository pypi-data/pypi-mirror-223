import numpy as np


from imagex.signal import bandpass_filter



def check_stability(vp, dt, dx):
    ''' Check the Courant number for stability condition
    '''

    # get the maximum velocity
    vp_max = np.max(vp)

    # check the Courant number before running the propagator
    Courant_number = vp_max * dt * np.sqrt(2.0) * (1.0 / 24.0 + 9.0 / 8.0) / dx

    if Courant_number > 1.0:
        msg = 'The Courant number is larger than 1.0.\n'
        msg += f'vp_max: {vp_max}, dt: {dt}, Courant number: {Courant_number}\n'
        msg += 'Reduce the time step size or increase the grid size'
        
        raise RuntimeError(msg)


def check_dispersion(vp, vs, dx, f0):
    ''' Check the numerical dispersion condition
    '''

    # get the minimum velocity
    if vs.max() > 0:
        v_min = np.min(vs[vs>0])
    else:   
        v_min = np.min(vp)

    dx0 = v_min / f0 / 4.
    f00 = v_min / dx / 4.

    # if dx0 < dx:
    #     # msg = 'Warning: numerical dispersion, dx = {:6.2f} m  > dx_required = {:6.2f} m \n'.format(dx, dx0)
    #     msg = 'Warning: numerical dispersion, f0 = {:6.2f} Hz > f0 max = {:6.2f} Hz \n'.format(f0, f00)
    #     print(msg)


def check_index_range(ind_x, ind_z, nx, nz, tag = 'source'):
    ''' Check the index range is inside the model
    '''
    if (ind_x.min() < 0 or
        ind_x.max() > nx or
        ind_z.min() < 0 or
        ind_z.max() > nz):

        msg = f'{tag} location is out of model range'

        raise ValueError(msg)


def pad_array(arr, npml, npad):
    ''' Pad a numpy array based on the number of PML layers and padding layers.
        The boundary values are extended from the original array.
    '''

    # Get the original shape of the array
    n_rows, n_cols = arr.shape

    # Create a new array with the padded dimensions
    padded_arr = np.zeros(
        (n_rows + 2 * npml + npad, n_cols + npml*2), dtype=arr.dtype)

    # Copy the original array into the padded array
    padded_arr[npml:n_rows+npml, npml:n_cols+npml] = arr

    # Fill the boundary values with corresponding values from the original array
    padded_arr[:npml, npml:-npml] = arr[0, :]
    padded_arr[-(npml+npad):, npml:-npml] = arr[-1, :]
    padded_arr[:, :npml] = padded_arr[:, npml].repeat(npml).reshape(-1, npml)
    padded_arr[:, -npml:] = padded_arr[:, -
                                       npml-1].repeat(npml).reshape(-1, npml)

    return padded_arr


def source_ricker(f, nStep, dt, t_delay=None):
    #  Ricker wavelet generation and integration for source
    #  Dongzhuo Li @ Stanford
    #  May, 2015

    e = np.pi * np.pi * f * f
    t_delay = 1.2/f if t_delay is None else t_delay

    source = np.zeros((nStep))
    amp = 1.0e7
    for it in range(0, nStep):
        source[it] = (1-2*e*(dt*(it)-t_delay)**2) * \
            np.exp(-e*(dt*(it)-t_delay)**2) * amp

    # change by Haipeng Li
    return source