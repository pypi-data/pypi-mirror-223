import numpy as np
from scipy.ndimage import gaussian_filter


def smooth2d(data, span=10):
    ''' Smooths values on 1D/2D/3D rectangular grid
    '''

    return gaussian_filter(data, sigma=span//2)


def print_time(worker, start_time, end_time):
    ''' Print the elapsed time
    '''

    hours, rem = divmod(end_time-start_time, 3600)
    minutes, seconds = divmod(rem, 60)
    print(f'{worker}: finished in {int(hours):0>2}h {int(minutes):0>2}m {seconds:.0f}s\n')


def check_shape(data, shape):
    ''' Check the shape of the data
    '''

    if data.shape != shape:
        raise ValueError(f'Wrong shape: {data.shape} != {shape}')


def calculate_double_difference(file1_path, file2_path, file3_path):
    ''' Calculate the double difference
    '''

    # Load the binary data from files (np.float32)
    file1 = np.fromfile(file1_path, dtype=np.float32)
    file2 = np.fromfile(file2_path, dtype=np.float32)
    file3 = np.fromfile(file3_path, dtype=np.float32)

    # Perform the calculation
    result = file1 - file2 + file3

    # Save the result to file3
    result.tofile(file3_path)


def merge_model(vp, vs, rho):
    ''' merge model
    '''

    model = np.concatenate((
        vp.flatten(),
        vs.flatten(),
        rho.flatten()))

    return model


def split_model(model, nx, nz):
    ''' separate model
    '''

    vp = model[:nx*nz].reshape(nz, nx)
    vs = model[nx*nz:-nx*nz].reshape(nz, nx)
    rho = model[-nx*nz:].reshape(nz, nx)

    return vp, vs, rho



def load_misfit(misfit_file):
    ''' Load the misfit from the file
    '''

    misfit = []
    with open(misfit_file) as f:
        for line in f:
            values = line.split()
            try:
                misfit.append(float(values[1]))
            except:
                pass
    return np.array(misfit)