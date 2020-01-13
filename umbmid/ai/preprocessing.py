"""
Tyson Reimer
University of Manitoba
July 30th, 2019
"""

import numpy as np

###############################################################################


def shuffle_arrays(arrays_list, rand_seed=0, return_seed=False):
    """Shuffle arrays to maintain inter-array ordering

    Shuffles each array in the list of arrays, arrays_list, such that
    the inter-array order is maintained (i.e., the zeroth element of
    the all arrays before shuffling corresponds to the nth element of
    all arrays after shuffling)

    Parameters
    ---------
    arrays_list : list
        List containing each array that will be shuffled
    rand_seed : int
        The seed to use for shuffling each array
    return_seed : bool
        If True, will return the seed used to shuffle the arrays (for
        reproducibility)

    Returns
    -------
    shuffled_arrs : list
        List containing the shuffled arrays
    rand_seed :
        The seed that was used to shuffle the arrays
    """

    shuffled_arrs = []  # Init arr for storing the shuffled arrays

    for array in arrays_list:  # For each array in the list
        np.random.seed(rand_seed)  # Set the seed

        if type(array) == list:  # If the 'array' is actually a list

            # Copy the list into a new var that will be shuffled
            shuffled_arr = [ii for ii in array]

        else:  # If the array is an array

            # Make a copy that will be shuffled
            shuffled_arr = array * np.ones_like(array)

        np.random.shuffle(shuffled_arr)  # Shuffle the array

        # Append the shuffled array to the list of shuffled arrays
        shuffled_arrs.append(shuffled_arr)

    if return_seed:  # If returning the seed, then do so
        return shuffled_arrs, rand_seed
    else:
        return shuffled_arrs


def normalize_samples(data):
    """Normalizes each sample in data to have unity maximum

    Parameters
    ----------
    data : array_like
        3D array of the features for each sample (assumes 2D features)

    Returns
    -------
    normalized_data : array_like
        Array of the features for each sample, normalized so that the
        max value is unity for each sample
    """

    # Assert that data must be 3D
    assert len(np.shape(data)) == 3, 'Error: data must have 3 dim'

    normalized_data = np.ones_like(data)  # Init array to return

    # For each sample
    for sample_idx in range(np.size(data, axis=0)):

        # Normalize to have max of unity
        normalized_data[sample_idx, :, :] = (data[sample_idx, :, :] /
                                             np.max(data[sample_idx, :, :]))

    return normalized_data
