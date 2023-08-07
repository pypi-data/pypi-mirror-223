#!/usr/bin/env python3

import sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

from imagex.utils.vector import Vector



def plot_das_sen(ind_das_x, ind_das_z, das_wt_x, das_wt_z, figsize=(10, 4), figname=None):
    ''' Plot source time function
    '''

    plt.figure(figsize=figsize)

    plt.subplot(1,2,1)
    cs = plt.scatter(ind_das_x, ind_das_z, c=das_wt_x, vmin=-1.0, vmax=1.0, cmap='jet', s=10)
    plt.colorbar(cs, orientation='horizontal', fraction=0.04, pad=0.08)
    plt.gca().invert_yaxis()

    plt.subplot(1,2,2)
    cs = plt.scatter(ind_das_x, ind_das_z, c=das_wt_z, vmin=-1.0, vmax=1.0, cmap='jet', s=10)
    plt.colorbar(cs, orientation='horizontal', fraction=0.04, pad=0.08)
    plt.gca().invert_yaxis()

    plt.tight_layout()

    if figname is not None:
        plt.savefig(figname, dpi=300)

    plt.show()
    plt.close()





def plot_stf(t, stf, fmax=50, figsize=(10, 3), figname=None):
    ''' Plot source time function
    '''

    plt.figure(figsize=figsize)
    plt.subplot(1,2,1)
    plt.plot(t, stf, 'b-')
    plt.xlabel('Time (s)')
    plt.ylabel('Amplitude')
    plt.title('Source Time Function')
    plt.grid(True)
    
    plt.subplot(1,2,2)
    dt = t[1] - t[0]
    n = len(t)
    freq = np.fft.fftfreq(n, dt)
    spectrum = np.abs(np.fft.fft(stf))
    idx = np.argsort(freq)
    idx = idx[int(len(idx) / 2):]
    
    plt.plot(freq[idx], spectrum[idx], 'r-')
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Amplitude')
    plt.title('Frequency Spectrum')
    plt.grid(True)
    plt.xlim(0, fmax)
    
    plt.tight_layout()

    if figname is not None:
        plt.savefig(figname, dpi=300)

    plt.show()
    plt.close()


def plot_misfit(misfit, semilogy=True, normalize=True, figsize=(8, 5), figname=None):
    ''' Plot misfit
    '''

    if normalize:
        misfit = misfit / misfit[0]

    plt.figure(figsize=figsize)
    if semilogy:
        plt.semilogy(misfit,  marker='o', linestyle='-', color='b')
    else:
        plt.plot(misfit,  marker='o', linestyle='-', color='b')
    plt.xlabel('Iteration')
    plt.ylabel('Misfit')
    plt.title('Misfit')
    plt.grid(True)
    plt.tight_layout()

    if figname is not None:
        plt.savefig(figname, dpi=300)
        
    plt.show()
    plt.close()





def plot_animation(data, clip=99.9, cmap='jet', aspect=1, width=10, height=6):
    ''' Plot wavefield

    Parameters
    ----------
    data : 3D numpy array
        data to plot (nt, nx, ny)
        nt = number of time steps
        nx = number of grid points in x-direction
        ny = number of grid points in y-direction
    '''

    # check if data is list or numpy array
    if isinstance(data, list):
        data = np.array(data)

    # check if wavefield is 3D
    if data.ndim != 3:
        raise ValueError('data must be 3D')

    # set clip
    clip_max = np.percentile(data, clip)
    # clip_min = np.percentile(data, 100-clip)

    clip_min = -clip_max

    fig = plt.figure(figsize=(width, height))
    ims = []

    for i in range(data.shape[0]):
        # set clip
        # clip_max = np.percentile(data[i], clip)
        # clip_min = np.percentile(data[i], 100-clip)

        im = plt.imshow(data[i], vmin=clip_min, vmax=clip_max,
                        aspect=aspect, cmap=cmap, animated=False)
        # add colorbar
        # plt.colorbar()
        ims.append([im])

    ani = animation.ArtistAnimation(
        fig, ims, interval=500, blit=True, repeat=True, repeat_delay=0)
    plt.close()

    return ani



# plot vector
if __name__ == '__main__':

    if len(sys.argv) < 2:
        print("Usage: python Plot.py <filename> or <filename1> <filename2>")
        sys.exit(1)

    if len(sys.argv) == 2:
        filename = sys.argv[1]
        vector = Vector.fromFile(filename)
        vector.plot()

    if len(sys.argv) == 3:
        filename1 = sys.argv[1]
        filename2 = sys.argv[2]

        vector1 = Vector.fromFile(filename1)
        vector2 = Vector.fromFile(filename2)
        vector3 = vector1 - vector2

        vector1.plot(more_data=[vector2, vector3])
