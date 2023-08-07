#!/usr/bin/env python3

import os
import numpy as np
import argparse

def add_noise_to_file(input_file, output_file, snr_db):
    # Load the data from the input file
    data = np.fromfile(input_file, dtype=np.float32)

    # Calculate the power of the original signal
    signal_power = np.mean(np.square(data))

    # Calculate the noise power from SNR
    noise_power = signal_power / (10 ** (snr_db / 10))

    # Generate random noise with the same shape as the original data
    noise = np.random.normal(loc=0.0, scale=np.sqrt(noise_power), size=data.shape)

    # Add noise to the original data
    noisy_data = data + noise

    # save as float32
    noisy_data.astype(np.float32).tofile(output_file)


def main(input_folder, snr_db, output_folder=None):

    # Set the default output folder if not provided
    if output_folder is None:
        
        # remove trailing slash
        if input_folder[-1] == '/':
            input_folder = input_folder[:-1]
        output_folder = f"{input_folder}_noise_{snr_db}dB"

    # Print the input and output folders
    print(f"Adding noise to data in {input_folder} with SNR = {snr_db} dB")
    print(f"Saving noisy data to {output_folder}")

    # Get a list of all .bin files in the input folder
    bin_files = [f for f in os.listdir(input_folder) if f.endswith('.bin')]

    # Create the output directory if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)

    # Loop through each .bin file and add noise
    for bin_file in bin_files:
        input_file = os.path.join(input_folder, bin_file)
        output_file = os.path.join(output_folder, os.path.basename(input_file))
        add_noise_to_file(input_file, output_file, snr_db)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Add noise to time series data.')
    parser.add_argument('input_folder', type=str, help='Path to the folder containing *.bin files')
    parser.add_argument('snr_db', type=float, help='Signal-to-Noise Ratio (SNR) in decibels')
    parser.add_argument('--output_folder', type=str, help='Path to the folder where noisy data will be saved. Default is "input_folder_snr".', default=None)

    args = parser.parse_args()

    main(args.input_folder, args.snr_db, args.output_folder)
