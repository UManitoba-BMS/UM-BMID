"""
Tyson Reimer
University of Manitoba
October 12th, 2019
"""

import os

from modules import get_proj_path, verify_path, get_script_logger
from modules.loadsave import save_pickle, save_mat, load_pickle
from modules.content import get_class_labels
from modules.ai.traintestsplit import split_to_train_test

###############################################################################

# Define the directory where the clean dataset is located
__DATA_DIR = os.path.join(get_proj_path(), 'datasets/gen-one/clean/')

###############################################################################

# Define the output directory where the train/test set files will
# be saved
__OUTPUT_DIR = os.path.join(get_proj_path(), 'datasets/gen-one/clean/')
verify_path(__OUTPUT_DIR)

###############################################################################

if __name__ == '__main__':

    logger = get_script_logger(__file__)  # Get logger

    # Load the dataset to be split and its metadata
    fd_data = load_pickle(os.path.join(__DATA_DIR, 'fd_data_s11_emp.pickle'))
    metadata = load_pickle(os.path.join(__DATA_DIR, 'md_list_s11_emp.pickle'))
    labels = get_class_labels(metadata)  # Get the class labels

    # Split into the train and test sets, and return the random seed
    # NOTE: The random seed that was used to make the train/test sets
    #       that produced the results presented in the EuCAP2020 paper
    #       is 909531601, and is set here for reproducibility.
    (train_data, test_data, train_labels, test_labels,
     train_md, test_md, seed) = split_to_train_test(fd_data, labels, metadata,
                                                    test_portion=0.2,
                                                    return_rand_seed=True,
                                                    init_seed=909531601,
                                                    logger=logger)

    # Save the files
    save_pickle(train_data,
                os.path.join(__OUTPUT_DIR, 'train_data.pickle'))
    save_pickle(train_md,
                os.path.join(__OUTPUT_DIR, 'train_md.pickle'))
    save_pickle(train_labels,
                os.path.join(__OUTPUT_DIR, 'train_labels.pickle'))
    save_pickle(test_data,
                os.path.join(__OUTPUT_DIR, 'test_data.pickle'))
    save_pickle(test_md,
                os.path.join(__OUTPUT_DIR, 'test_md.pickle'))
    save_pickle(test_labels,
                os.path.join(__OUTPUT_DIR, 'test_labels.pickle'))

    save_mat(train_data, 'train_data',
             os.path.join(__OUTPUT_DIR, 'train_data.mat'))
    save_mat(train_md, 'train_md',
             os.path.join(__OUTPUT_DIR, 'train_md.mat'))
    save_mat(train_labels, 'train_labels',
             os.path.join(__OUTPUT_DIR, 'train_labels.mat'))
    save_mat(test_data, 'test_data',
             os.path.join(__OUTPUT_DIR, 'test_data.mat'))
    save_mat(test_md, 'test_md',
             os.path.join(__OUTPUT_DIR, 'test_md.mat'))
    save_mat(test_labels, 'test_labels',
             os.path.join(__OUTPUT_DIR, 'test_labels.mat'))
