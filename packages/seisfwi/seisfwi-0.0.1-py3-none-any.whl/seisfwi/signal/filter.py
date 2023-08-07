#!/usr/bin/env python3


import argparse
import os
import numpy as np
from scipy.signal import butter, filtfilt, lfilter
from multiprocessing import Pool


# from numba import jit

from imagex.utils import load_sg


# @jit(nopython=True)
def bandpass_filter(data, lowcut, highcut, dt, order=4):
    '''Butterworth bandpass filter from scipy Cookbook

    Parameters
    ----------
        data: 1D array of float
            the data to be filtered
        lowcut: float
            the lowcut frequency
        highcut: float
            the highcut frequency
        dt: float
            the sampling interval
        order: int
            the order of the filter (default: 4)

    Returns
    -------
        data_bp: 1D array of float
            the filtered data
    '''

    fs = 1.0 / dt
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='band')
    data_bp = filtfilt(b, a, data)

    # print("Using lfilter instead of filtfilt!")
    # data_bp = lfilter(b, a, data)

    return np.asarray(data_bp, dtype=np.float32)


# @jit(nopython=True)
def lowpass_filter(data, highcut, dt, order=4):
    '''Butterworth lowpass filter from scipy Cookbook

    Parameters
    ----------
        data: 1D array of float
            the data to be filtered
        highcut: float
            the highcut frequency
        dt: float
            the sampling interval
        order: int
            the order of the filter (default: 4)

    Returns
    -------
        data_bp: 1D array of float
            the filtered data
    '''

    fs = 1.0 / dt
    nyq = 0.5 * fs
    high = highcut / nyq
    b, a = butter(order, high, btype='low')
    data_lp = filtfilt(b, a, data)

    return np.asarray(data_lp, dtype=np.float32)

# @jit(nopython=True) 
def highpass_filter(data, lowcut, dt, order=4):
    '''Butterworth highpass filter from scipy Cookbook

    Parameters
    ----------
    data: 1D array of float
        the data to be filtered
    lowcut: float
        the lowcut frequency
    dt: float
        the sampling interval
    order: int
        the order of the filter (default: 4)

    Returns
    -------
        data_bp: 1D array of float
            the filtered data
    '''

    fs = 1.0 / dt
    nyq = 0.5 * fs
    low = lowcut / nyq
    b, a = butter(order, low, btype='hp')
    data_hp = filtfilt(b, a, data)

    return np.asarray(data_hp, dtype=np.float32)


# @jit(nopython=True)
def process_file(input_file, output_file, lowcut, highcut, nt, dt):
    ''' Process a single .bin file
    '''
    
    print(f"Filtering {input_file} ...")

    # Load the data from the .bin file
    data = load_sg(input_file, nt)

    # Apply the filter based on the filter type and frequency range
    for i in range(data.shape[0]):
        data[i] = bandpass_filter(data[i], lowcut, highcut, dt, order=4)

    # save as float32
    data.astype(np.float32).tofile(output_file)


def main(input_folder, lowcut, highcut, nt, dt, output_folder, nproc):

    # Set the default output folder if not provided
    if output_folder is None:
        # remove trailing slash
        if input_folder[-1] == '/':
            input_folder = input_folder[:-1]
        output_folder = f"{input_folder}_bp_{lowcut}_{highcut}Hz"

    # Print the input and output folders
    print(f"Filtering data in {input_folder} with bandpass filter {lowcut} - {highcut} Hz, nt={nt}, dt={dt}, with {nproc} processors")
    print(f"Saving filtered data to {output_folder}")

    # Create the output directory if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)

    # Get a list of all .bin files in the input folder
    bin_files = [f for f in os.listdir(input_folder) if f.endswith('.bin')]

    # # Loop through each .bin file and add noise
    # for bin_file in bin_files:
    #     input_file = os.path.join(input_folder, bin_file)
    #     output_file = os.path.join(output_folder, bin_file)

    #     print(f"Filtering {input_file} ...")
    #     process_file(input_file, output_file, lowcut, highcut, nt, dt)

    # use multiprocessing to process all files in parallel
    pool = Pool(nproc)

    # create a list of arguments for each file
    args = [(os.path.join(input_folder, bin_file),
             os.path.join(output_folder, bin_file),
             lowcut, highcut, nt, dt) for bin_file in bin_files]
    
    # run the process_file function in parallel
    pool.starmap(process_file, args)

    # close the pool
    pool.close()
    pool.join()




if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Filter time series data from *.bin files.")

    parser.add_argument("input_folder", type=str, help="Path to the input folder containing *.bin files.")
    parser.add_argument("lowcut", type=float, help="Lower frequency limit for the bandpass filter.")
    parser.add_argument("highcut", type=float, help="Upper frequency limit for the bandpass filter.")
    parser.add_argument("nt", type=int, help="Number of time samples.")
    parser.add_argument("dt", type=float, help="Time sampling interval.")
    parser.add_argument("--nproc", type=int, help="Number of processors to use. Default is 1.", default=1)
    parser.add_argument('--output_folder', type=str, help='Path to the folder where noisy data will be saved. Default is "input_folder_snr".', default=None)

    args = parser.parse_args()

    main(args.input_folder, args.lowcut, args.highcut,
         args.nt, args.dt, args.output_folder, args.nproc)


#TODO: add mpi4py support or dask support or process pool support