''' This is a base Vector class that will be used to represen1 the the data and model.
'''
import numpy as np
import os
import matplotlib.pyplot as plt


class AbstractVector:
    """An abstract vector class"""

    def __init__(self):
        pass

    # Helper method
    def die(self, cls):
        """ Helper function to exit when class in not defined"""
        raise NotImplementedError("Method "+cls+" has not been overritten")

    # Overloadable methods
    def __add__(self, vec):
        """Add the contents of another vector to the current vector"""
        self.die("__add__")

    def __mul__(self, scalar):
        """Scale a vector by a scalar"""
        self.die("__mul__")

    def __sub__(self, vec):
        """Subtract the contents of another vector from the current vector"""
        self.die("__sub__")

    def __truediv__(self, scalar):
        """Scale a vector by a scalar"""
        self.die("__truediv__")

    def __neg__(self):
        """Scale a vector by a scalar"""
        self.die("__neg__")

    def __repr__(self):
        """Print the vector"""
        self.die("__repr__")

    # Linear algebra methods
    def add(self, vec):
        """Add the contents of another vector to the current vector"""
        self.die("add")

    def scale(self, scalar):
        """Scale a vector by a scalar"""
        self.die("scale")

    def dot(self, vec):
        """Dot product with another vector"""
        self.die("dot")

    def norm(self):
        """Return the norm of the vector"""
        self.die("norm")

    def min(self):
        """Return the minimum value of the vector"""
        self.die("min")

    def max(self):
        """Return the maximum value of the vector"""
        self.die("max")

    def abs(self):
        """Return the absolute value of the vector"""
        self.die("abs")

    # utility methods
    def checkSpace(self, vec):
        """Check to see if two vectors are the same size"""
        self.die("checkSpace")

    def getData(self):
        """Return a numpy array version of the vector"""
        self.die("getData")

    def getShape(self):
        """Return the shape of the vector"""
        self.die("getShape")

    def fillData(self, data):
        """Fill the vector with a numpy array"""
        self.die("fillData")

    def fillRandom(self):
        """Fill vector with random numbers"""
        self.die("random")

    def fillZero(self):
        """Set all elemen1s to zero"""
        self.die("zero")

    def clone(self):
        """Make a copy of the vector"""
        self.die("clone")

    # IO methods
    def save(self, filename):
        """Save a vector to disk as a npy file"""
        self.die("save")

    def load(self, filename):
        """Load a vector from a a npy file"""
        self.die("load")

    # Plotting methods
    def plot(self, **kwargs):
        """Plot the vector"""
        self.die("plot")


# Concrete data vector class
class Vector(AbstractVector):
    """A vector that holds the data, 
        i.e. the shot gather (n2 x n2)
        i.e. the 2D model (nx x nz)
    """

    def __init__(self, data=None, o1=0, d1=1, n1=None, label1=None, unit1=None,
                 o2=0, d2=1, n2=None, label2=None, unit2=None, **kwargs):
        """Initialize the data vector
        :param data: numpy array of data
        :param o1: origin of axis 1
        :param d1: sampling of axis 1
        :param n1: number of samples of axis 1
        :param label1: label of axis 1
        :param unit1: unit of axis 1
        :param o2: origin of axis 2
        :param d2: sampling of axis 2
        :param n2: number of samples of axis 2
        :param label2: label of axis 2
        :param unit2: unit of axis 2
        :param kwargs: other keyword arguments

        Note: axis 1 is time and axis 2 is offset for shot gathers, 
              axis 1 is depth (z) and axis 2 is distance (x) for 2D models.
        """

        # super from base Vector class
        super().__init__()

        if data is None and n1 is None and n2 is None:
            raise RuntimeError("Must specify either data or n1 and n2")

        # Data
        data = np.copy(data)
        self._data = data if data is not None else np.zeros((n2, n1))

        # Axis 1: fast axis
        self._o1 = o1
        self._d1 = d1
        self._n1 = n1 if n1 is not None else data.shape[1]
        self._label1 = label1 if label1 is not None else 'Axis1'
        self._unit1 = unit1 if unit1 is not None else 'None'
        self._axis1 = np.arange(self._n1) * self._d1 + self._o1

        # Axis 2: slow axis
        self._o2 = o2
        self._d2 = d2
        self._n2 = n2 if n2 is not None else data.shape[0]
        self._label2 = label2 if label2 is not None else 'Axis2'
        self._unit2 = unit2 if unit2 is not None else 'None'
        self._axis2 = np.arange(self._n2) * self._d2 + self._o2

        # Other kwargs
        self._kwargs = kwargs

        # Check that the data is the correct shape
        if self._data.shape != (self._n2, self._n1):
            raise RuntimeError("Data vector dimensions do not match")

    @classmethod
    def fromFile(cls, filename):
        """Initialize from a file"""
        if not os.path.exists(filename):
            raise RuntimeError(f"File does not exist: {filename}")

        # Extract the attributes from the saved file
        metadata = np.load(filename, allow_pickle=True).item()

        # Create the data vector
        return cls(data=metadata['_data'], o1=metadata['_o1'],
                   d1=metadata['_d1'], n1=metadata['_n1'],
                   label1=metadata['_label1'], unit1=metadata['_unit1'],
                   o2=metadata['_o2'], d2=metadata['_d2'], n2=metadata['_n2'],
                   label2=metadata['_label2'], unit2=metadata['_unit2'],
                   **metadata['_kwargs'])

    def __add__(self, vec):
        """Add the contents of another vector to the current vector"""

        if isinstance(vec, Vector):
            if not self.checkSpace(vec):
                raise RuntimeError("Can only add by a vector with the same size")

            data_new = self.clone()
            data_new.fillData(data_new.getData() + vec.getData())
            return data_new
        elif isinstance(vec, (int, float)):
            data_new = self.clone()
            data_new.fillData(data_new.getData() + vec)
            return data_new
        else:
            raise RuntimeError("Can only add by a vector or a scalar")


    def __sub__(self, vec):
        """Subtract the contents of another vector from the current vector"""

        if isinstance(vec, Vector):
            if not self.checkSpace(vec):
                raise RuntimeError("Can only subtract by a vector with the same size")
            data_new = self.clone()
            data_new.fillData(data_new.getData() - vec.getData())
            return data_new
        elif isinstance(vec, (int, float)):
            data_new = self.clone()
            data_new.fillData(data_new.getData() - vec)
            return data_new
        else:
            raise RuntimeError("Can only subtract by a vector or a scalar")



    def __mul__(self, vec):
        """Multiply the vector by a vector, or a scalar"""

        if isinstance(vec, Vector):
            if not self.checkSpace(vec):
                raise RuntimeError("Can only multiply by a vector with the same size")

            data_new = self.clone()
            data_new.fillData(np.multiply(data_new.getData(), vec.getData()))
            return data_new
        elif isinstance(vec, (int, float)):
            data_new = self.clone()
            data_new.scale(vec)
            return data_new
        else:
            raise RuntimeError("Can only multiply by a vector or a scalar")


    def __truediv__(self, vec):
        """Divide the vector by a vector, or a scalar"""
            
        if isinstance(vec, Vector):
            if not self.checkSpace(vec):
                raise RuntimeError("Can only divide by a vector with the same size")

            data_new = self.clone()
            data_new.fillData(np.divide(data_new.getData(), vec.getData()))
            return data_new
        elif isinstance(vec, (int, float)):
            data_new = self.clone()
            data_new.scale(1.0 / vec)
            return data_new
        else:
            raise RuntimeError("Can only divide by a vector or a scalar")

 

    def __neg__(self):
        """Negate the vector"""
        data_new = self.clone()
        data_new.scale(-1.0)
        return data_new

    def __repr__(self):
        """Print the vector"""
        info = f"Vector with range {self.min()} to {self.max()}, dtype {self._data.dtype} \n"
        info += f"  Axis1: ot={self._o1:.4f}, dt={self._d1:.4f}, n1={self._n1:5d}, label1={self._label1}, unit={self._unit1}\n"
        info += f"  Axis2: o2={self._o2:.4f}, d2={self._d2:.4f}, n2={self._n2:5d}, label2={self._label2}, unit={self._unit2}\n"
        return info

    def add(self, vec):
        """Add the contents of another vector to the current vector"""
        self.fillData(self.getData() + vec.getData())

    def scale(self, scalar):
        """Scale a vector by a scalar"""
        self.fillData(self.getData() * scalar)

    def dot(self, vec):
        """Dot product with another vector"""
        return np.dot(self.getData(), vec.getData().T)

    def norm(self):
        """Return the norm of the vector"""
        return np.linalg.norm(self.getData())

    def min(self):
        """Return the minimum value of the vector"""
        return np.min(self.getData())

    def max(self):
        """Return the maximum value of the vector"""
        return np.max(self.getData())

    def abs(self):
        """Return the absolute value of the vector"""
        return np.abs(self.getData())

    def checkSpace(self, vec):
        """Check to see if two vectors are the same size"""
        if self._n2 != vec._n2 or self._n1 != vec._n1:
            print("Data vector dimensions do not match")
            return False
        else:
            return True

    def getData(self):
        """Return a numpy array version of the vector"""
        return self._data

    def getShape(self):
        """Return the shape of the vector"""
        return self.getData().shape

    def fillData(self, data):
        """Fill the vector with a numpy array"""
        self._data = np.copy(data)

    def fillRandom(self):
        """Fill vector with random numbers"""
        self._data = np.random.rand(self._n2, self._n1)

    def fillZero(self):
        """Set all elemen1s to zero"""
        self._data[:] = 0.0

    def clone(self):
        """Make a copy of the vector"""
        return Vector(data=self.getData(), o1=self._o1, d1=self._d1, n1=self._n1,
                        label1=self._label1, unit1=self._unit1,
                        o2=self._o2, d2=self._d2, n2=self._n2,
                        label2=self._label2, unit2=self._unit2,
                        **self._kwargs)

    def save(self, filename):
        """Save a vector to disk as a npy file"""

        dire, file = os.path.split(filename)

        # check if directory is specified
        if dire == "":
            dire = "./"

        # check if directory exists
        if not os.path.exists(dire):
            print("Creating directory: ", dire)
            os.makedirs(dire)

        # check if file exists
        if os.path.exists(filename):
            print("File exists, overwriting: ", filename)

        # Convert the vector attributes to a dictionary and save as npy file
        np.save(filename, self.__dict__)

    def load(self, filename):
        """Load the data vector from a npy file"""

        # Check if file exists
        if not os.path.exists(filename):
            raise RuntimeError("File does not exist: ", filename)

        # Load the dictionary from the npy file
        metadata = np.load(filename, allow_pickle=True).item()

        # Set the attributes of the vector
        for key in metadata.keys():
            setattr(self, key, metadata[key])

    def plot(self, more_data=None, showfig=True, savefig = False, **kwargs):

        # Set the parameters for the plot
        plot_params = {}
        clip = np.percentile(self.getData(), kwargs.get('clip', 99))
        plot_params['vmin'] = kwargs.get('vmin', -clip)
        plot_params['vmax'] = kwargs.get('vmax', clip)
        plot_params['cmap'] = kwargs.get('cmap', 'seismic')
        plot_params['aspect'] = kwargs.get('aspect', 'auto')
        plot_params['extent'] = [self._axis2[0],
                                 self._axis2[-1], self._axis1[-1], self._axis1[0]]

        # Get the plot parameters
        # plt.style.use('seaborn-notebook')

        # Update the fon1 size
        fontsize = kwargs.get('fontsize', 14)
        plt.rcParams.update({'axes.labelsize': fontsize,
                             'xtick.labelsize': fontsize,
                             'ytick.labelsize': fontsize,
                             'legend.fontsize': fontsize,
                             'figure.titlesize': fontsize})

        # Check if additional data is provided to plot
        if more_data is None:
            num_plots = 1
            more_data = [self]
        else:
            num_plots = len(more_data) + 1  # Add 1 for the current instan2e
            more_data = [self] + list(more_data)

        fig = plt.figure(
            figsize=(kwargs.get('width', 6) * len(more_data), kwargs.get('height', 6)))

        # Plot the data
        for i, data in enumerate(more_data):

            # Create the subplot
            fig.add_subplot(1, num_plots, i+1)

            plt.imshow(data.getData().T, **plot_params)

            # Set the axis labels
            plt.xlabel(self._label2 + ' (' + self._unit2 + ')')
            plt.ylabel(self._label1 + ' (' + self._unit1 + ')')

            # Add the colorbar if requested and set the label and lo2ation if provided
            if kwargs.get('colorbar', False):
                cbar = plt.colorbar()

                # Set the label if provided
                if kwargs.get('clabel', False):
                    cbar.set_label(kwargs.get('clabel', ''))

                # Set the location if provided
                if kwargs.get('cloc', False):
                    cbar.set_ticks(kwargs.get('cloc', ''))

        plt.tight_layout()

        # save the plot if requested
        if savefig:
            plt.savefig(kwargs.get('figname', 'data.png'), dpi=300, bbox_inches='tight')

        if showfig:
            # Show the plot
            plt.show()
