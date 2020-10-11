"""
Tyson Reimer
University of Manitoba
July 17th, 2019
"""

import os
import numpy as np
import pandas as pd

from umbmid import null_logger, get_proj_path
from umbmid.loadsave import load_fd_data
from umbmid.sigproc import iczt

###############################################################################

__DATA_DIR = os.path.join(get_proj_path(), 'datasets\\')

###############################################################################

# This dict maps the headers for each info-piece contained in the
# metadata files to the corresponding Python datatype
dtypes_dict = {
                'n_expt': int,
                'id': int,
                'phant_id': str,
                'tum_rad': float,
                'tum_shape': str,
                'tum_x': float,
                'tum_y': float,
                'tum_z': float,
                'birads': int,
                'adi_vol': float,
                'fib_vol': float,
                'adi_ref_id': int,
                'emp_ref_id': int,
                'date': str,
                'n_session': int,
                'ant_rad': float,
                'ant_z': float,
                'fib_ang': float,
                'adi_x': float,
                'adi_y': float,
                'fib_ref_id': int,
                'fib_x': float,
                'fib_y': float,
                'tum_in_fib': int
            }

###############################################################################


def import_metadata(gen='one'):
    """Load the metadata of each expt as a dict, return as list of dicts

    Loads the -metadata.csv files for each experimental session and
    creates a list of the metadata dict for each individual experiment.

    Parameters
    ----------
    gen : str
        The generation of data to import, must be in ['one', 'two']

    Returns
    -------
    metadata : list
        List of the metadata dict for each expt
    """

    assert gen in ['one', 'two'], \
        "Error: gen must be in ['one', 'two']"

    this_data_dir = os.path.join(__DATA_DIR, 'gen-%s/raw/' % gen)

    metadata = []  # Init list to return

    # For each experimental session in the dataset
    for expt_session in os.listdir(this_data_dir):

        # If the expt_session is a directory
        if os.path.isdir(os.path.join(this_data_dir, expt_session)):

            # Get the path to the -metadata.csv file for this
            # expt_session
            metadata_path = os.path.join(this_data_dir, expt_session,
                                         expt_session + '-metadata.csv')

            # Load the -metadata.csv file for this expt_session
            session_metadata = np.genfromtxt(metadata_path, delimiter=',',
                                             dtype=str)

            # Get the keys for the metadata
            metadata_keys = session_metadata[0, :]

            for md_key in metadata_keys:

                # Assert the metadata str is valid
                assert md_key in dtypes_dict.keys(), \
                    "Error: invalid metadata str %s in file %s" % (
                        md_key, metadata_path
                    )

            # For each individual scan within this expt_session
            for expt in range(1, np.size(session_metadata, axis=0)):

                # Get the metadata values (as str's) for this expt
                expt_metadata = session_metadata[expt, :]

                expt_metadata_dict = dict()  # Init dict for this expt

                # Create counter for the different pieces of metadata
                # info
                info_counter = 0

                # For each info piece in the metadata
                for info_piece in metadata_keys:

                    # If the value for this info piece is NOT missing
                    if not expt_metadata[info_counter] == '':

                        # Store the value as its proper dtype
                        expt_metadata_dict[info_piece] = \
                            dtypes_dict[info_piece](
                                expt_metadata[info_counter])

                    else:  # If the value for this info piece IS missing

                        assert info_piece in dtypes_dict.keys(), \
                                '%s not valid info-piece, in file: %s' \
                                % (info_piece, metadata_path)

                        # If the dtype for this info piece is an int
                        # or float, store as NaN
                        if (dtypes_dict[info_piece] == int or
                                dtypes_dict[info_piece] == float):

                            expt_metadata_dict[info_piece] = np.NaN

                        # If the dtype for this info piece is a str,
                        # store as empty str
                        else:
                            expt_metadata_dict[info_piece] = ''

                    info_counter += 1  # Increase the info counter

                # Append the metadata dict for this expt to the list
                metadata.append(expt_metadata_dict)

    return metadata


def import_fd_dataset(gen='one', sparams='s11', logger=null_logger):
    """Load the freq-domain s-params of each sample in the dataset

    Loads the .txt raw data files of the measured S-parameters in the
    frequency domain for each scan, and returns as an array.

    Parameters
    ----------
    gen : str
        The generation of dataset to use, must be in ['one', 'two']
    sparams : str
        Must be in ['s11', 's21'], indicates which type of s-param to
        import
    logger :
        Logging object for recording progress

    Returns
    -------
    fd_dataset : array_like
        The S-parameters in the frequency-domain for each scan
    """

    assert sparams in ['s11', 's21'], \
        "Error: sparams must be in ['s11', 's21']"

    assert gen in ['one', 'two'], \
        "Error: gen must be in ['one', 'two']"

    this_data_dir = os.path.join(__DATA_DIR, 'gen-%s/raw/' % gen)

    if sparams in ['s11']:
        sparam_str = 'Mono'
    else:
        sparam_str = 'Multi'

    # Init list for storing the S-parameters for each scan
    fd_dataset = []

    # For each experimental session in the dataset
    for expt_session in os.listdir(this_data_dir):

        # If the expt_session is a directory
        if os.path.isdir(os.path.join(this_data_dir, expt_session)):

            logger.info('Working on:\t%s...' % expt_session)

            # Get the path to the -metadata.csv file for this
            # expt_session
            metadata_path = os.path.join(this_data_dir, expt_session,
                                         expt_session + '-metadata.csv')

            # Load the -metadata.csv file for this expt_session
            session_metadata = np.genfromtxt(metadata_path, delimiter=',',
                                             dtype=str)

            # Get the identifying strings for each experiment in
            # this session as described in the -metadata.csv file
            expt_strs = ['expt%2d' % int(ii) for ii in session_metadata[1:, 0]]

            # Use format 'expt01', 'expt02', etc.
            expt_strs = [ii.replace(' ', '0') for ii in expt_strs]

            # Find the files that are possible experiments
            potential_expts = os.listdir(os.path.join(this_data_dir,
                                                      expt_session))

            # For each potential experiment (file in the session folder)
            for expt in potential_expts:

                # If this is not the -metadata.csv file, and if
                # the file is of the target sparam  ('s11' or 's21')
                if '-metadata.csv' not in expt and sparam_str in expt:

                    logger.info('\t\tLoading expt:\t%s' % expt)

                    # Find the expt name from the .txt file name
                    expt_name = expt.split('_')[1].lower()

                    # Assert that the expt_name matches one of the expts
                    # described in the -metadata.csv file
                    assert expt_name in expt_strs, \
                        'Error: file %s not expected experiment for ' \
                        'session %s' % (expt, expt_session)

                    # If the scan was performed counterclockwise, it
                    # has the identifier string '(foC'
                    if '(foC' in expt.split('_'):

                        # For any counterclockwise scans, convert them
                        # to being clockwise
                        fd_dataset.append(
                            np.flip(load_fd_data(
                                os.path.join(this_data_dir, expt_session,
                                             expt)), axis=1))

                    else:  # If the scan was performed clockwise
                        fd_dataset.append(
                            load_fd_data(os.path.join(this_data_dir,
                                                      expt_session, expt)))

    # Convert the frequency-domain dataset to an np array
    fd_dataset = np.reshape(fd_dataset,
                            [len(fd_dataset), fd_dataset[0].shape[0],
                             fd_dataset[0].shape[1]])

    return fd_dataset


def import_fd_cal_dataset(cal_type='emp', prune=True, gen='two', sparams='s11',
                          logger=null_logger):
    """Load the calibrated freq-domain s-params of each expt in dataset

    Loads the .txt raw data files of the measured S-parameters in the
    frequency domain for each scan, then subtracts off a calibration
    scan (either empty-chamber calibration or adipose calibration) and
    returns as an array

    Parameters
    ----------
    cal_type : str
        The type of calibration scan to subtract - expected to be in
        ['emp', 'adi']. If 'emp', uses an empty-chamber
        calibration scan, if 'adi' uses an adipose-only phantom
        calibration scan.
    prune : bool
        If True, will return an array containing only the scans that
        were of phantoms containing a fibroglandular component and that
        had a valid reference scan.
    gen : str
        Must be in ['one', 'two'], specifies the generation of data to
        import
    sparams : str
        The sparams to import, must be in ['s11', 's21']
    logger :
        Logger for logging progress

    Returns
    -------
    cal_dataset : array_like
        Array of calibrated data
    cal_metadata : list
        List of calibrated metadata
    """

    assert cal_type in ['emp', 'adi'], \
        "Error: cal_type must be in ['emp', 'adi']"

    assert gen in ['one', 'two'], \
        "Error: gen must be in ['one', 'two']"

    assert sparams in ['s11', 's21'], \
        "Error: sparams must be in ['s11', 's21']"

    # If using an adipose-only phantom calibration scan
    if cal_type in ['adi']:
        cal_str = 'adi_ref_id'  # Set the cal_str to indicate this

    else:  # If using an empty-chamber calibration scan
        cal_str = 'emp_ref_id'  # Set the cal_str to indicate this

    # Load the freq-domain dataset
    fd_dataset = import_fd_dataset(sparams=sparams,
                                   gen=gen,
                                   logger=logger)

    # Import the metadata for the scans in the dataset
    metadata = import_metadata(gen=gen)

    cal_dataset = np.zeros_like(fd_dataset)  # Init array to return

    for expt_idx in range(len(metadata)):  # For each experiment

        # Get the metadata for this expt
        this_expt_metadata = metadata[expt_idx]

        # Get the unique_id number of the reference scan for this expt
        this_expt_ref_num = this_expt_metadata[cal_str]

        ref_idx = -1

        # Look through all other expts to find the expt with the
        # unique_id number matching the reference for expt_idx
        for second_expt_idx in range(len(metadata)):

            # If the unique_id of this second_expt matches the
            # unique_id of the reference
            if metadata[second_expt_idx]['id'] == this_expt_ref_num:

                # Assign this to be the temporary index of the
                # reference scan
                ref_idx = second_expt_idx

        # If the expt corresponding to expt_idx has a reference scan
        if not np.isnan(this_expt_ref_num):

            assert ref_idx >= 0, ('Error: no ref found for unique ID %d' %
                                  this_expt_metadata['id'])

            # Get the reference expt frequency-domain data for this
            # expt_idx
            ref_expt = fd_dataset[ref_idx, :, :]

            # Get the frequency-domain data for this expt_idx
            this_expt = fd_dataset[expt_idx, :, :]

            # Subtract the reference
            cal_dataset[expt_idx, :, :] = this_expt - ref_expt

    # If pruning the dataset to include scans that had a fibroglandular
    # component and had a valid calibration scan
    if prune:

        # Init lists for storing the samples in the pruned dataset and
        # the metadata of these samples
        pruned_dataset = []
        cal_metadata = []

        for expt_idx in range(len(metadata)):  # For each sample

            # If the phantom contains fibroglandular tissue AND has a
            # valid reference scan
            if ('F' in metadata[expt_idx]['phant_id'] and
                    not np.isnan(metadata[expt_idx][cal_str])):

                # Append this sample to the list of samples
                pruned_dataset.append(cal_dataset[expt_idx, :, :])
                cal_metadata.append(metadata[expt_idx])

        # Convert the dataset to an np array
        cal_dataset = np.reshape(pruned_dataset,
                                 [len(pruned_dataset),
                                  pruned_dataset[0].shape[0],
                                  pruned_dataset[0].shape[1]])

    else:  # If *NOT* pruning the dataset

        # Set the metadata to be returned as the metadata for all the
        # experiments
        cal_metadata = metadata

    return cal_dataset, cal_metadata


def convert_to_idft_dataset(fd_dataset):
    """Convert the freq-domain data to the time-domain via the IDFT

    Converts each sample in the fd_dataset from the frequency-domain
    to the time-domain via the IDFT.

    Parameters
    ----------
    fd_dataset : array_like
        The measured S-parameters in the frequency domain for each
        sample in the dataset

    Returns
    -------
    idft_dataset : array_like
        The time-domain representation of the data for each sample in
        the dataset, obtained via the IDFT
    """

    idft_dataset = np.zeros_like(fd_dataset)  # Init array to return

    # For each sample in the dataset
    for expt_idx in range(fd_dataset.shape[0]):

        print('\t\tWorking on expt [%4d / %4d]' % (expt_idx + 1,
                                                   fd_dataset.shape[0]))

        # Convert to the time-domain via the IDFT
        idft_dataset[expt_idx, :, :] = np.fft.ifft(fd_dataset[expt_idx, :, :],
                                                   axis=0)

    return idft_dataset


def convert_to_iczt_dataset(fd_dataset, num_time_pts=1024, start_time=0.0,
                            stop_time=6e-9, ini_freq=1e9, fin_freq=8e9,
                            logger=null_logger):
    """Convert the freq-domain data to the time-domain via the ICZT

    Converts each sample in the fd_dataset from the frequency-domain to
    the time-domain via the ICZT

    Parameters
    ----------
    fd_dataset : array_like
       The measured S-parameters in the frequency domain for each
       sample in the dataset
    num_time_pts : int
        The number of points in the time domain used to represent the
        signal
    start_time : float
        The starting time of the time-domain signals, in seconds
    stop_time : float
        The stopping time of the time-domain signals, in seconds
    ini_freq : float
        The initial frequency used in the scan, in Hz
    fin_freq : float
        The final frequency used in the scan, in Hz
    logger :
        Logger for logging the progress

    Returns
    -------
    iczt_dataset : array_like
        The time-domain representation of the data for each sample in
        the dataset, obtained via the ICZT
    """

    # Init array to return
    iczt_dataset = np.zeros([fd_dataset.shape[0], num_time_pts,
                             fd_dataset.shape[2]], dtype=complex)

    # For each sample in the datasets
    for expt_idx in range(fd_dataset.shape[0]):

        logger.info('\t\tWorking on expt [%4d / %4d]' %
                    (expt_idx + 1, fd_dataset.shape[0]))

        # Convert the sample to the time-domain via the ICZT
        iczt_dataset[expt_idx, :, :] = iczt(fd_dataset[expt_idx, :, :],
                                            start_time, stop_time,
                                            num_time_pts, ini_freq, fin_freq)

    return iczt_dataset


def get_info_piece_list(metadata, info_str):
    """Return list of values for specific info piece from metadata

    Returns a list of the values for a specific info piece
    (specified by info_str) for each sample whose metadata is in the
    list metadata.

    Parameters
    ----------
    metadata : list
        List containing the metadata dict for each sample
    info_str : str
        The string specifying the info piece of interest

    Returns
    -------
    info_list : array_like
        The value of the info piece for each sample whose metadata was
        contained in the metadata list
    """

    assert info_str in dtypes_dict.keys(), \
        'Error: info_str was %s, invalid value' % info_str

    # Get a list of the specified info piece
    info_list = [md[info_str] for md in metadata]

    return np.array(info_list)


def import_metadata_df(gen='one'):
    """Loads the metadata and returns as a pandas dataframe.

    Parameters
    ----------
    gen : str
        The generation of data, must be in ['one', 'two']

    Returns
    -------
    metadata :
        The metadata of the experiments, returned as a pandas dataframe.
    """

    assert gen in ['one', 'two'], \
        "Error: gen must be in ['one', 'two']"

    # Load the metadata as a list of dicts
    metadata = import_metadata(gen=gen)

    metadata_df = pd.DataFrame()  # Init dataframe to return

    # For each info-piece in the metadata
    for metadata_info in metadata[0].keys():

        # Make this a column
        metadata_df[metadata_info] = get_info_piece_list(metadata,
                                                         metadata_info)

    return metadata_df
