"""
Tyson Reimer
University of Manitoba
October 21st, 2019
"""

import os
import numpy as np

from umbmid import get_proj_path, verify_path, get_script_logger
from umbmid.loadsave import save_pickle, save_mat
from umbmid.build import (import_fd_dataset, import_metadata,
                          import_metadata_df)

###############################################################################

__OUTPUT_DIR = os.path.join(get_proj_path(), 'datasets/')
verify_path(__OUTPUT_DIR)

__DATA_DIR = os.path.join(get_proj_path(), 'datasets/')

###############################################################################

# The possible sparams for each generation of dataset
possible_sparams = {
    'one': ['s11'],
    'two': ['s11', 's21'],
}

###############################################################################

if __name__ == '__main__':

    logger = get_script_logger(__file__)

    logger.info('Beginning...Construction of All Data Clean Files...')

    for gen in ['one', 'two']:

        logger.info('\tWorking on gen-%s...' % gen)

        # The output path for this generation of dataset
        output_here = os.path.join(__OUTPUT_DIR,
                                   'gen-%s/simple-clean/' % gen)
        verify_path(output_here)

        # Get the list of the possible sparams for this gen
        sparams_here = possible_sparams[gen]

        for sparam in sparams_here:  # For each sparam

            logger.info('\t\tWorking on sparam %s...' % sparam)

            # Import the frequency-domain data for every scan in the
            # dataset
            fd_data = import_fd_dataset(gen=gen,
                                        sparams=sparam,
                                        logger=logger)

            # Import the metadata as a list of dicts and as
            # pandas dataframe
            metadata = import_metadata(gen=gen)
            metadata_df = import_metadata_df(gen=gen)

            logger.info('\t\t\tFD data of num samples:\t%d'
                        % np.size(fd_data, axis=0))
            logger.info('\t\t\tMetadata of num samples:\t%d'
                        % len(metadata))

            # Save the frequency-domain and metadata to .pickle files
            save_pickle(fd_data, os.path.join(output_here,'python-data',
                                              'fd_data_gen_%s_%s.pickle'
                                              % (gen, sparam)))
            save_pickle(metadata, os.path.join(output_here, 'python-data/',
                                               'metadata_gen_%s.pickle'
                                               % gen))
            save_pickle(metadata_df, os.path.join(output_here, 'python-data/',
                                                  'metadata_df_gen_%s.pickle'
                                                  % gen))

            # Save the frequency-domain and metadata to .mat files
            save_mat(fd_data, 'fd_data',
                     os.path.join(output_here, 'matlab-data/',
                                  'fd_data_gen_%s_%s.mat' % (gen, sparam)))
            save_mat(metadata, 'metadata',
                     os.path.join(output_here, 'matlab-data/',
                                  'metadata_gen_%s.mat' % gen))
