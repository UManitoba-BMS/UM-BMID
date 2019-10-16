"""
Tyson Reimer
University of Manitoba
July 26th, 2019
"""

import pickle
import scipy.io as scio
import numpy as np

###############################################################################


def load_fd_data(data_path):
    """Load raw .txt file into array of complex freq-domain s-params

    Loads a raw data .txt file and returns the measured complex
    S-parameters in the frequency domain.

    Parameters
    ----------
    data_path : str
        Path to the data file to load

    Returns
    -------
    fd_data : array_like
        The measured complex S-parameters in the frequency domain
    """

    # Load the .txt file into an array
    raw_data = np.genfromtxt(data_path, dtype=float, delimiter='')

    # Find the number of freqs and twice the number of scan positions
    num_freqs, num_scan_positions = raw_data.shape

    # Find the number of scan positions (typically 72)
    num_scan_positions //= 2

    # Init array to return
    fd_data = np.zeros([num_freqs, num_scan_positions], dtype=complex)

    # For each scan position
    for scan_position in range(num_scan_positions):

        # Combine the real and imag parts from the .txt file
        fd_data[:, scan_position] = (raw_data[:, 2 * scan_position]
                                     + 1j * raw_data[:, 2 * scan_position + 1])

    return fd_data


def save_pickle(var, path):
    """Saves the var to the path as a .pickle file

    Parameters
    ----------
    var :
        The variable to be saved
    path : str
        The full path to the saved .pickle file
    """

    with open(path, 'wb') as handle:
        pickle.dump(var, handle, protocol=pickle.HIGHEST_PROTOCOL)


def save_mat(var, var_name, path):
    """Saves the var to the path as a .mat file

    Parameters
    ----------
    var :
        The variable to be saved
    var_name : str
        Str used as the name for the var in the .mat file
    path : str
        The full path to the saved .mat file
    """

    scio.savemat(path, {var_name: var})


def load_pickle(path):
    """Loads the .pickle file located at path

    Parameters
    ----------
    path : str
        The full path to the .pickle file that will be loaded

    Returns
    -------
    loaded_var :
        The loaded variable
    """

    with open(path, 'rb') as handle:
        loaded_var = pickle.load(handle)

    return loaded_var
