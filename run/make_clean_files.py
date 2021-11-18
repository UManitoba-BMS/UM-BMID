"""
Tyson Reimer
University of Manitoba
October 13th, 2019
"""

import os
import numpy as np

from umbmid import get_proj_path, verify_path, get_script_logger, null_logger
from umbmid.loadsave import save_pickle, save_mat
from umbmid.build import import_fd_cal_dataset
from umbmid.sigproc import iczt

###############################################################################

__OUTPUT_DIR = os.path.join(get_proj_path(),
                            'datasets/')
verify_path(__OUTPUT_DIR)

###############################################################################


def make_clean_files(gen='one', cal_type='emp', sparams='s11',
                     logger=null_logger):
    """Makes and saves the clean .mat and .pickle files

    Parameters
    ----------
    gen : str
        The generation of data to be used, must be in ['one', 'two']
    cal_type : str
        The type of calibration to be performed, must be in
        ['emp', 'adi'
    sparams : str
        The type of sparam to save, must be in ['s11', 's21']
    logger :
        A logger for logging progress
    """

    assert gen in ['one', 'two', 'three'], \
        "Error: gen must be in ['one', 'two', 'three']"

    assert sparams in ['s11', 's21'], \
        "Error: sparams must be in ['s11', 's21']"

    # Load the frequency-domain dataset
    logger.info('\tImporting FD data and metadata...')
    fd_data, fd_md = import_fd_cal_dataset(cal_type=cal_type,
                                           prune=True,
                                           gen=gen,
                                           sparams=sparams,
                                           logger=logger)

    logger.info('\tImport complete. Saving to .pickle and .mat files...')

    # Define an output dir for this generation of dataset
    this_output_dir = os.path.join(__OUTPUT_DIR,
                                   'gen-%s/clean/' % gen)
    verify_path(this_output_dir)  # Verify that this dir exists

    logger.info('Num data samples:\t\t%s' % np.size(fd_data, axis=0))
    logger.info('Length of metadata:\t\t%s' % len(fd_md))

    # Save the frequency-domain data and metadata
    save_pickle(fd_md,
                os.path.join(this_output_dir, 'md_list_%s_%s.pickle' %
                             (sparams, cal_type)))
    save_pickle(fd_data,
                os.path.join(this_output_dir, 'fd_data_%s_%s.pickle' %
                             (sparams, cal_type)))
    save_mat(fd_data, 'fd_data_%s' % sparams,
             os.path.join(this_output_dir, 'fd_data_%s_%s.mat'
                          % (sparams, cal_type)))
    save_mat(fd_md, 'md_%s' % sparams,
                os.path.join(this_output_dir, 'md_list_%s_%s.mat'
                             % (sparams, cal_type)))

    logger.info('\tComplete saving clean data files.')


###############################################################################

if __name__ == '__main__':

    our_logger = get_script_logger(__file__)

    for cal_type in ['emp', 'adi']:
    # for cal_type in ['adi']:

        for gen in ['three']:  # For each generation of dataset

            if gen in ['two', 'three']:  # If the second generation

                # S11 and S21 are possible sparams
                possible_sparams = ['s11', 's21']

            else:  # If the first generation

                # S11 is only possible sparams
                possible_sparams = ['s11']

            for sparams in possible_sparams:  # For each possible sparam

                make_clean_files(gen=gen,
                                 sparams=sparams,
                                 cal_type=cal_type,
                                 logger=our_logger)
