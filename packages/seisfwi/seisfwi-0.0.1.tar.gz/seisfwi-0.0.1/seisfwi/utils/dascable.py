
import numpy as np
import matplotlib.pyplot as plt


# TODO: compute the DAS response based on computed vx, vy, vz
#       and prepare the adjoint source for the DAS data
#       pass the dot-product test


class DASCable(object):
    ''' methods associated with DAS modeling and inversion

    Parameters
    ----------
    :param ndarray trajectory: the trajectory of the das cable, ndarray with shape (npts, ndim==3)
    :param int nx: number of grid points in x direction, default is None
    :param int ny: number of grid points in y direction, default is None
    :param int nz: number of grid points in z direction, default is None
    :param float dh: grid spacing in x, y, and z direction, default is None
    '''

    def __init__(self, trajectory, gauge_length, nx=None, ny=None, nz=None, dh=None):

        # check the input trajectory
        if trajectory.shape[1] != 3:
            raise ValueError(
                "trajectory must be a 3D array with shape (npts, 3)")

        if trajectory.shape[0] < 2:
            raise ValueError("trajectory must have at least 2 points")

        # check existence of duplicate coordinates
        unique_points = set(tuple(coord) for coord in trajectory)
        if len(unique_points) != trajectory.shape[0]:
            raise ValueError("trajectory contains duplicate coordinates")

        # check gauge length
        if gauge_length <= 0:
            raise ValueError("gauge_length must be positive")

        # set the dimension of the das cable
        if np.any(trajectory[:, 1] != 0):
            self.ndim = 3
        else:
            self.ndim = 2

        # set the trajectory and gauge length
        self._traj_control = np.copy(trajectory)
        self._gauge_length = gauge_length

        # set the spatial coordinate
        if nx is None or nz is None or dh is None:
            self.x = np.linspace(np.min(
                self._traj_control[:, 0]) - 10, np.max(self._traj_control[:, 0]) + 10, num=100, endpoint=False)
            self.y = np.linspace(np.min(
                self._traj_control[:, 1]) - 10, np.max(self._traj_control[:, 1]) + 10, num=100, endpoint=False)
            self.z = np.linspace(np.min(
                self._traj_control[:, 2]) - 10, np.max(self._traj_control[:, 2]) + 10, num=100, endpoint=False)
        else:
            self.x = np.linspace(0, dh*nx, num=nx, endpoint=False)
            self.y = np.linspace(0, dh*ny, num=ny, endpoint=False)
            self.z = np.linspace(0, dh*nz, num=nz, endpoint=False)

        if self.ndim == 2:
            self.y = np.zeros_like(self.x)

        # interpolate the trajectory at every gauge length
        self._traj_interp, self._chordlen = interparc(
            self._traj_control, self._gauge_length, method='linear', verbose=True)

        # # insert the control points into interpolated points, based on the distance

        # compute the tangent vectors of the control points
        self._tangent_control = frenet_serret(
            self._traj_control[:, 0], self._traj_control[:, 1], self._traj_control[:, 2])

        # compute the tangent vectors of the interpolated points
        self._tangent_interp = frenet_serret(
            self._traj_interp[:, 0], self._traj_interp[:, 1], self._traj_interp[:, 2])

    def get_interp_trajectory(self):
        ''' get the interpolated points of the das cable
        '''

        return self._traj_interp

    def get_arclength(self):
        ''' get the arclength of the das cable
        '''

        return self._chordlen

    def get_tangent(self):
        ''' get the tangent vectors of the das cable at the interpolated points
        '''

        return self._tangent_interp

    def plot_trajectory(self, show_interp=False, show_tangent=False,
                        grid_on=True, aspect='auto', xmin=None, xmax=None):

        # Two dimensions (plane curve)
        if self.ndim == 2:

            if show_interp:
                data = [self._traj_control, self._traj_interp]
                colors = ['r', 'b']
                lines = ['-o', '-o']
                titles = ['Control points', 'Interpolated points']
                figsize = (16, 8)
            else:
                data = [self._traj_control]
                colors = ['r']
                lines = ['-o']
                titles = ['Control points']
                figsize = (8, 8)

            fig = plt.figure(figsize=figsize)
            for i, d in enumerate(data):
                ax = fig.add_subplot(1, len(data), i+1)
                ax.plot(d[:, 0], d[:, 2], lines[i], color=colors[i],
                        linewidth=0.8, markersize=3.0)

                if show_tangent and i == 0:  # plot the tangent vectors of the control points
                    ax.quiver(d[:, 0], d[:, 2], self._tangent_control[:, 0], -
                              self._tangent_control[:, 2], color='k', scale=30.0, width=0.003)
                elif show_tangent and i == 1:  # plot the tangent vectors of the interpolated points
                    ax.quiver(d[:, 0], d[:, 2], self._tangent_interp[:, 0], -
                              self._tangent_interp[:, 2], color='k', scale=30.0, width=0.003)
                # Note: I added the minus sign to flip the z axis, so that the depth is positive downward

                ax.grid(grid_on)
                ax.set_aspect(aspect)
                ax.set_xlim([self.x[0], self.x[-1]])
                ax.set_ylim([self.z[-1], self.z[0]])
                ax.set_xlabel('Distance (m)', fontsize=12)
                ax.set_ylabel('Depth (m)', fontsize=12)
                ax.set_title(titles[i], fontsize=12)
                if xmin is not None and xmax is not None:
                    ax.set_xlim([xmin, xmax])
                # ax.invert_yaxis()

            plt.tight_layout()
            plt.show()

        # Three dimensions (space curve)
        elif self.ndim == 3:
            if show_interp:
                data = [self._traj_control, self._traj_interp]
                colors = ['r', 'b']
                lines = ['-o', '-o']
                titles = ['Control points', 'Interpolated points']
                figsize = (16, 8)
            else:
                data = [self._traj_control]
                colors = ['r']
                lines = ['-o']
                titles = ['Control points']
                figsize = (8, 8)

            fig = plt.figure(figsize=figsize)
            for i, d in enumerate(data):
                ax = fig.add_subplot(1, len(data), i+1, projection='3d')
                ax.plot(d[:, 0], d[:, 1], d[:, 2], lines[i], color=colors[i],
                        linewidth=0.8, markersize=3.0)

                scale = 0.05 * self.get_arclength()

                if show_tangent and i == 0:    # show the tangent vectors of the control points
                    ax.quiver(d[:, 0], d[:, 1], d[:, 2], self._tangent_control[:, 0], self._tangent_control[:, 1],
                              self._tangent_control[:, 2], color='k', length=scale, normalize=True)
                elif show_tangent and i == 1:  # show the tangent vectors of the interpolated points
                    ax.quiver(d[:, 0], d[:, 1], d[:, 2], self._tangent_interp[:, 0], self._tangent_interp[:, 1],
                              self._tangent_interp[:, 2], color='k', length=scale, normalize=True)

                ax.grid(grid_on)
                ax.set_aspect(aspect)
                ax.set_xlim([self.x[0], self.x[-1]])
                ax.set_ylim([self.y[0], self.y[-1]])
                ax.set_zlim([self.z[-1], 0.0])
                ax.set_xlabel('Distance (m)', fontsize=12, color='k')
                ax.set_ylabel('Distance (m)', fontsize=12, color='k')
                ax.set_zlabel('Depth (m)', fontsize=12, color='k')

            plt.tight_layout()
            plt.show()

    def plot_sensitivity(self, grid_on=True, cmap='plasma', aspect='auto'):

        # Two dimensions (plane curve)
        if self.ndim == 2:
            figsize = (16, 8)
            fig = plt.figure(figsize=figsize)

            data = [self._tangent_interp[:, 0], self._tangent_interp[:, 2]]
            titles = ['Sensitivity to Vx', 'Sensitivity to Vz']
            for i, d in enumerate(data):
                ax = fig.add_subplot(1, len(data), i+1)
                cs = ax.scatter(self._traj_interp[:, 0], self._traj_interp[:, 2],
                                c=d, vmin=-1.0, vmax=1.0, cmap=cmap, s=10)
                # add colorbar to the bottom of the figure, tight
                plt.colorbar(cs, orientation='horizontal',
                             fraction=0.04, pad=0.08)

                ax.grid(grid_on)
                ax.set_aspect(aspect)
                ax.set_xlim([self.x[0], self.x[-1]])
                ax.set_ylim([self.z[-1], 0.0])
                ax.set_xlabel('Distance (m)', fontsize=12)
                ax.set_ylabel('Depth (m)', fontsize=12)
                ax.set_title(titles[i], fontsize=16)
                # ax.invert_yaxis()

            plt.tight_layout()
            plt.show()

        # Three dimensions (space curve)
        elif self.ndim == 3:
            figsize = (16, 8)
            fig = plt.figure(figsize=figsize)

            data = [self._tangent_interp[:, 0],
                    self._tangent_interp[:, 1], self._tangent_interp[:, 2]]
            titles = ['Sensitivity to Vx',
                      'Sensitivity to Vy', 'Sensitivity to Vz']
            for i, d in enumerate(data):
                ax = fig.add_subplot(1, len(data), i+1, projection='3d')
                cs = ax.scatter(self._traj_interp[:, 0], self._traj_interp[:, 1], self._traj_interp[:, 2],
                                c=d, vmin=-1.0, vmax=1.0, cmap=cmap, s=10)
                plt.colorbar(cs, orientation='horizontal',
                             fraction=0.04, pad=0.08)

                ax.grid(grid_on)
                ax.set_aspect(aspect)
                ax.set_xlim([self.x[0], self.x[-1]])
                ax.set_ylim([self.y[0], self.y[-1]])
                ax.set_zlim([self.z[-1], 0.0])
                ax.set_xlabel('Distance (m)', fontsize=10, color='k')
                ax.set_ylabel('Distance (m)', fontsize=10, color='k')
                ax.set_zlabel('Depth (m)', fontsize=10, color='k')
                ax.set_title(titles[i], fontsize=16)

            plt.tight_layout()
            plt.show()


    def forward(self, waveforms):
        ''' Compute the forward modeling of the DAS data based on the calculated 
            waveforms in the components of particle velocity (vx, vy, vz)
        '''
        raise NotImplementedError
    

    def adjoint(self, data):
        ''' Compute the adjoint source for the DAS data
        '''
        raise NotImplementedError
    
    
    def dot_product_test(self, waveforms, data):
        ''' Compute the dot product test between the forward modeling and 
            the adjoint source
        '''
        raise NotImplementedError


# partition_of_unity_property
def interparc(p, gl, method='linear', verbose=True):
    """
    Interpolate points along a curve in 2 or more dimensions.

    Parameters
    ----------
    :param np.array p: coordinates of the points defining the curve to be interpolated, of shape (npts, 3)
    :param float gl: the desired gauge length of the interpolated points
    :param str method: the interpolation method to use, either 'linear' or 'spline'
    :param bool verbose: whether to print out the estimated number of points and the averaged error

    Returns
    -------
    :return np.array pt: the interpolated points

    """

    # check method
    valid_methods = ['linear', 'spline']

    if method not in valid_methods:
        raise ValueError(f"method must be one of {valid_methods}")
    elif method == 'spline':
        raise NotImplementedError(
            "Spline interpolation is not yet implemented")

    # check gl
    if gl <= 0:
        raise ValueError("gl must be positive")

    # check p
    npts = p.shape[0]
    ndim = p.shape[1]

    if ndim not in [2, 3]:
        raise ValueError("p must be 2D or 3D")

    if npts < 2:
        raise ValueError("p must have at least 2 points")

    # Calculate the approximated npts
    chordlen_all = np.sqrt(np.sum(np.diff(p, axis=0) ** 2, axis=1))
    chordlen = np.sum(chordlen_all)

    if chordlen <= gl:
        raise ValueError(
            f"Gauge length {gl} must be smaller than the length of the curve {chordlen}")

    nt = int(np.floor(chordlen / gl))

    print("Before adjust: ", p[-1])
    print(nt)

    # adjust the last point to make sure the arc length is evenly divided by gl

    # length of gl * (nt-1)
    chordlen_desired = gl * nt

    # calculate the distance needed to be adjusted to the last point
    d = chordlen_desired - chordlen + chordlen_all[-1]

    # calculate the unit vector of the last segment
    u = (p[-1] - p[-2]) / chordlen_all[-1]

    # add the distance to the last point, assuming the last segment is straight
    p[-1] = p[-2] + d * u

    # calculate the new chord length
    chordlen_all = np.sqrt(np.sum(np.diff(p, axis=0) ** 2, axis=1))
    chordlen = np.sum(chordlen_all)

    nt = int(np.floor(chordlen / gl)) + 1

    print("After adjust: ", p[-1])

    # interpolate the curve with the desired number of points
    pt = interpolate_curve(nt, p, npts, ndim)

    if verbose:
        # calculate the error with the desired gauge length
        error = np.mean(
            abs(np.sqrt(np.sum(np.diff(pt, axis=0) ** 2, axis=1)) - gl))
        print(f"Desired gauge length: {gl}")
        print(f"Number of points: {nt}, with averaged error: {error:.6f}")

    # dudt = (p[tbins] - p[tbins-1]) / chordlen[tbins-1][:, np.newaxis]

    return pt, chordlen


def interpolate_curve(nt, p, npts, ndim):
    ''' Interpolate a curve with nt points from p with npts points
    '''

    t = np.linspace(0, 1, nt)

    pt = np.full((nt, ndim), np.nan)
    chordlen = np.sqrt(np.sum(np.diff(p, axis=0)**2, axis=1))
    chordlen /= np.sum(chordlen)
    cumarc = np.hstack((0, np.cumsum(chordlen)))

    tbins = np.digitize(t, cumarc)
    tbins[(tbins <= 0) | (t <= 0)] = 1
    tbins[(tbins >= npts) | (t >= 1)] = npts - 1
    s = (t - cumarc[tbins-1]) / chordlen[tbins-1]
    pt = p[tbins-1] + (p[tbins] - p[tbins-1]) * s[:, np.newaxis]

    return pt


def frenet_serret(x, y, z):
    ''' Calculate the Frenet-Serret Space Curve Invariants
        _    r'
        T = ----  (Tangent)
            |r'|

        _    T'
        N = ----  (Normal)
            |T'|
        _   _   _
        B = T x N (Binormal)

        k = |T'|  (Curvature)

        t = dot(-B',N) (Torsion)

    if z is None, then it is assumed to be zero, acording to the 2D case.
    But the equations are still valid for 2D case.

    '''

    # Check input
    if x.shape != y.shape != z.shape:
        raise ValueError("x, y, z must have the same shape")

    # Convert to column vectors
    x = x.flatten()
    y = y.flatten()
    z = z.flatten()

    # Speed of curve
    dx = np.gradient(x)
    dy = np.gradient(y)
    dz = np.gradient(z)
    dr = np.vstack((dx, dy, dz)).T

    ddx = np.gradient(dx)
    ddy = np.gradient(dy)
    ddz = np.gradient(dz)
    ddr = np.vstack((ddx, ddy, ddz)).T

    # Tangent
    T = dr / mag(dr, 3)

    # Note: the code below is benchmarked with MATLAB code:
    # FRENET - Frenet-Serret Space Curve Invarients
    # The Tanget is very accurate, while the Normal and Binormal both have
    # some descrepancies, only at a few points. I check the reason and it is
    # because of division of two very small numbers. I think it is fine to
    # ignore these descrepancies.

    # Derivative of tangent
    dTx = np.gradient(T[:, 0])
    dTy = np.gradient(T[:, 1])
    dTz = np.gradient(T[:, 2])
    dT = np.vstack((dTx, dTy, dTz)).T

    # Normal
    # the division of two very small numbers may cause some descrepancies
    N = dT / mag(dT, 3)

    # Binormal
    B = np.cross(T, N)

    # Curvature
    k = mag(np.cross(dr, ddr), 1) / ((mag(dr, 1))**3)

    # Torsion
    t = -np.einsum('ij,ij->i', B, N)

    # Return the normal
    return T


def mag(T, n):
    ''' Magnitude of a vector (Nx3)
    '''

    M = np.linalg.norm(T, axis=1)
    d = np.where(M == 0)[0]
    M[d] = np.finfo(float).eps * np.ones_like(d)
    M = M[:, np.newaxis]
    M = np.tile(M, (1, n))

    return M
