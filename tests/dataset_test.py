"""
Tyson Reimer
University of Manitoba
October 15th, 2019
"""

import os

from umbmid import get_proj_path, get_script_logger

###############################################################################

__DATA_DIR = os.path.join(get_proj_path(), 'datasets/')

###############################################################################

possible_gens = ['one',
                 'two',
                 ]

possible_data_types = [
    'clean',
    'raw',
]

possible_clean_names = {'one': ['fd_data_s11_adi.mat',
                                'fd_data_s11_adi.pickle',
                                'idft_data_s11_adi.mat',
                                'idft_data_s11_adi.pickle',
                                'iczt_data_s11_adi.mat',
                                'iczt_data_s11_adi.pickle',
                                'md_list_s11_adi.pickle',
                                'fd_data_s11_emp.mat',
                                'fd_data_s11_emp.pickle',
                                'idft_data_s11_emp.mat',
                                'idft_data_s11_emp.pickle',
                                'iczt_data_s11_emp.mat',
                                'iczt_data_s11_emp.pickle',
                                'md_list_s11_emp.pickle',
                                ],
                        'two': ['fd_data_s11_adi.mat',
                                'fd_data_s11_adi.pickle',
                                'idft_data_s11_adi.mat',
                                'idft_data_s11_adi.pickle',
                                'iczt_data_s11_adi.mat',
                                'iczt_data_s11_adi.pickle',
                                'fd_data_s21_adi.mat',
                                'fd_data_s21_adi.pickle',
                                'idft_data_s21_adi.mat',
                                'idft_data_s21_adi.pickle',
                                'iczt_data_s21_adi.mat',
                                'iczt_data_s21_adi.pickle',
                                'md_list_s11_adi.pickle',
                                'fd_data_s11_emp.mat',
                                'fd_data_s11_emp.pickle',
                                'idft_data_s11_emp.mat',
                                'idft_data_s11_emp.pickle',
                                'iczt_data_s11_emp.mat',
                                'iczt_data_s11_emp.pickle',
                                'fd_data_s21_emp.mat',
                                'fd_data_s21_emp.pickle',
                                'idft_data_s21_emp.mat',
                                'idft_data_s21_emp.pickle',
                                'iczt_data_s21_emp.mat',
                                'iczt_data_s21_emp.pickle',
                                'md_list_s11_emp.pickle',
                                ]}

###############################################################################

if __name__ == '__main__':

    logger = get_script_logger(__file__)

    logger.info('Beginning...DATA VERIFICATION...')

    n_folders_here = 0  # Init var for storing num folders that exist

    for gen in ['one', 'two']:  # For each gen of dataset

        # See if the gen dir exists
        dir_exists = os.path.isdir(os.path.join(__DATA_DIR,
                                                'gen-%s/' % gen))

        if dir_exists:  # If the gen dir does exist
            logger.info('\tSuccess. gen-%s/ exists.' % dir_exists)

            for data_type in ['clean', 'raw']:  # For each data type

                # See if the subfolder exists
                subdir_exists = os.path.isdir(os.path.join(__DATA_DIR,
                                                           'gen-%s/%s'
                                                           % (gen, data_type)))
                if subdir_exists:  # If the subfolder exists
                    logger.info('\t\tgen-%s/%s/ exists:\t%s'
                                % (gen, data_type, subdir_exists))
                    n_folders_here += 1  # Increment counter

                else:  # If the subfolder does not exist
                    logger.info('\t\tFAILURE: folder /gen-%s/%s/ does not '
                                'exist.' % (gen, data_type))

        else:  # If the gen dir does not exist
            logger.info('\tFAILURE: folder /gen-%s/ does not exist.' % gen)

    if n_folders_here == 4:  # If all folders exist

        logger.info('Success! All folders exist.')
        logger.info('Verifying clean data files...')

        for gen in possible_gens:  # For each gen dir

            # Get the dir here
            this_dir = os.path.join(__DATA_DIR, 'gen-%s/clean/' % gen)

            # For each file name that should exist
            for clean_name in possible_clean_names[gen]:

                # Check if the file exists
                file_exists = os.path.isfile(os.path.join(this_dir,
                                                          clean_name))

                if file_exists:  # If the file does exist, report it
                    logger.info('\tSuccess. File /gen-%s/clean/%s exists.' %
                                (gen, clean_name))

                else:  # If the file does not exist, report it
                    logger.info('\t\tFAILURE. File /gen-%s/clean/%s does not '
                                'exist.' % (gen, clean_name))
