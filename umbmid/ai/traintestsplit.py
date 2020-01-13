"""
Tyson Reimer
University of Manitoba
July 22nd, 2019
"""

import numpy as np

from umbmid import null_logger
from umbmid.ai.preprocessing import shuffle_arrays

########################################################################

__ADI_IDS = [
    'A1',
    'A2',
    'A3',
]

__N_ADI = len(__ADI_IDS)

########################################################################


def verify_train_test_sets(train_metadata, test_metadata):
    """Verify no duplicate samples in train/test sets

    Verifies that no sample in the test set has a corresponding sample
    in the training set with identical phantom_id, tum_size, and
    tumor position

    Parameters
    ----------
    train_metadata : list
        List of the metadata dict for each sample in the training set
    test_metadata : list
        List of the metadata dict for each sample in the test set

    Returns
    -------

    """

    # Make a list containing tuples of the phantom_id, tum_size, and
    # tumor positions for each sample in the train and test sets
    train_constraint_info = [(md['phant_id'][:2], md['tum_rad'],
                              md['tum_x'], md['tum_y'])
                             for md in train_metadata]
    test_constraint_info = [(md['phant_id'][:2], md['tum_rad'],
                             md['tum_x'], md['tum_y'])
                            for md in test_metadata]

    # Find if ay samples in the test set have the same phantom_id,
    # tum_size and tumor position as a sample in the train set
    unique_test = any(sample in train_constraint_info for sample in
                      test_constraint_info)

    return unique_test


def split_to_train_test(data, labels, metadata, test_portion=0.2, init_seed=-1,
                        return_rand_seed=False, logger=null_logger):
    """Split dataset into train/test portions

    Splits the dataset (comprised of the data, labels, and metadata)
    into training and testing sets, ensuring class balance, BI-RADS
    class balance, and tumor-size balance in the test set.

    Parameters
    ----------
    data : array_like
        The measurements for each sample in the dataset (could be in
        frequency-domain or time-domain)
    labels : array_like
        The class labels (0 or 1; no-tumor or tumor) for each sample
        in the dataset
    metadata : list
        The metadata dict for each sample in the dataset
    test_portion : float
        The portion of the dataset that will be used to form the test
        set (must be between 0 and 1)
    init_seed : int
        If positive, will be used as the rand seed during shuffling
    return_rand_seed : bool
        If True, will return the seed used to generate the successful
        train/test set split
    logger : logging_object
        Logger for displaying the progress


    Returns
    -------
    train_data : array_like
        The data for each sample in the training set
    test_data : array_like
        The data for each sample in the test set
    train_labels : array_like
        The class label (0 for no-tumor, 1 for tumor) of each sample in
        the training set
    test_labels : array_like
        The class label (0 for no-tumor, 1 for tumor) of each sample in
        the test set
    train_metadata : list
        List containing the metadata dicts for each sample in the
        training set
    test_metadata : list
        List containing the metadata dicts for each sample in the
        training set
    """

    # Assert that the value for test_portion is correct
    assert 0 < test_portion < 1, \
        'Error: test_portion value %.2e is invalid, must be between ' \
        '0 and 1' % test_portion

    # Init var for if the test-set conditions have been satisfied
    test_conditions_satisfied = False

    # Find the num of training samples to use
    num_train_samples = int(data.shape[0] * (1 - test_portion))
    num_test = int(data.shape[0] - num_train_samples)

    # Make lists for the tum sizes, BI-RADS classes
    tum_sizes = [md['tum_rad'] for md in metadata]
    birads_classes = [md['birads'] for md in metadata]

    logger.info('\tBeginning search for test set that satisfies conditions...')

    # Init flag for the first time shuffling the arrays
    first_shuffle = True

    rand_seed = 0  # Init rand seed

    # Init arrays to return
    (train_data, test_data, train_labels, test_labels, train_metadata,
     test_metadata) = [], [], [], [], [], []

    # Until the test-set satisfies the conditions
    while not test_conditions_satisfied:

        # If the first time and an init seed provided, then use it
        if first_shuffle and init_seed >= 0:
            logger.debug('first shuffle')
            # Shuffle the set
            [shuffled_data, shuffled_labels, shuffled_metadata,
             shuffled_tum_sizes, shuffled_biards], rand_seed = \
                shuffle_arrays([data, labels, metadata, tum_sizes,
                                birads_classes], return_seed=True,
                               rand_seed=init_seed)

            first_shuffle = False  # Change flag for the first shuffle

        else:  # Otherwise, shuffle with random seed
            rand_seed = np.random.randint(1000000000)
            logger.debug('rand seed:\t%s' % rand_seed)

            [shuffled_data, shuffled_labels, shuffled_metadata,
             shuffled_tum_sizes, shuffled_biards], rand_seed = \
                shuffle_arrays([data, labels, metadata, tum_sizes,
                                birads_classes], return_seed=True,
                               rand_seed=rand_seed)  # Shuffle the set

        # Convert the lists to arrays
        shuffled_labels = np.array(shuffled_labels)
        shuffled_metadata = np.array(shuffled_metadata)

        # Find the indices of the positive and negative samples
        pos_samples = np.where(shuffled_labels == 1)[0].astype('int')
        neg_samples = np.where(shuffled_labels == 0)[0].astype('int')

        # Force the first num_test positive and negative samples to be
        # in the test set
        test_idxs = np.concatenate((pos_samples[:num_test // 2],
                                    neg_samples[:num_test // 2])
                                   ).astype('int')

        # Force the rest of the samples to be in the training set
        train_idxs = np.concatenate((pos_samples[num_test // 2:],
                                     neg_samples[num_test // 2:])
                                    ).astype('int')

        # Get the train and test data/labels/metadata after shuffling
        test_data = shuffled_data[test_idxs, :, :]
        test_labels = shuffled_labels[test_idxs]
        test_metadata = shuffled_metadata[test_idxs]
        train_data = shuffled_data[train_idxs, :, :]
        train_labels = shuffled_labels[train_idxs]
        train_metadata = shuffled_metadata[train_idxs]

        # Verify that the train and test sets have no samples with
        # tumors of the same size, in the same phantom, at the same
        # position
        unique_test = verify_train_test_sets(train_metadata, test_metadata)

        # If there are no such duplicate samples, verify that the other
        # conditions are satisfied
        if unique_test:

            logger.info('\t\tSplit successful. Checking if split '
                        'satisfies conditions...')

            # Find the tumor sizes and BI-RADS classes of the test
            # samples
            test_tum_sizes, test_birads = \
                (shuffled_tum_sizes[num_train_samples:],
                 shuffled_biards[num_train_samples:])

            # num_test = len(test_labels)  # The number of test samples

            # The number of positive test samples
            num_pos = np.sum(test_labels)

            # The fraction of test samples that are positive
            frac_test_pos = num_pos / num_test

            # Verify that the class balance is as desired
            class_balance = 0.49 < frac_test_pos < 0.51

            # Find the number of 1 cm and 2 cm tumors in the test set
            num_1cm = np.sum(np.array(test_tum_sizes) == 1)
            num_2cm = np.sum(np.array(test_tum_sizes) == 2)
            num_3cm = np.sum(np.array(test_tum_sizes) == 3)

            test_adi_ids = dict()  # Init dict for storing adi IDs

            for test_adi_id in __ADI_IDS:  # For each adipose shell ID

                # Find the # of test samples with this adipose ID
                test_adi_ids[test_adi_id] = \
                    np.sum([test_adi_id in md['phant_id']
                            for md in test_metadata])

            adi_balance = False  # Init flag for adipose shell balance

            # Init number of balanced adipose shell IDs
            num_adi_balanced = 0
            for adi_id in test_adi_ids.keys():  # For each adi ID

                # If this is 'balanced'
                if (0.75 * num_test / __N_ADI < test_adi_ids[adi_id]
                        < 1.25 * num_test / __N_ADI):
                    num_adi_balanced += 1  # Increment num balanced

            if num_adi_balanced == __N_ADI:  # If all balanced
                adi_balance = True  # Set flag for balance to True

            # Check if the tumor sizes are balanced as desired
            tum_size_balance = (0.2 * num_pos < num_1cm < 0.4 * num_pos and
                                0.2 * num_pos < num_2cm < 0.4 * num_pos and
                                0.2 * num_pos < num_3cm < 0.4 * num_pos)

            # Find the number of BI-RADS Class I/II/III/IV samples in
            # the test set
            num_c1 = np.sum(np.array(test_birads) == 1)
            num_c2 = np.sum(np.array(test_birads) == 2)
            num_c3 = np.sum(np.array(test_birads) == 3)
            num_c4 = np.sum(np.array(test_birads) == 4)

            # Check if the BI-RADS classes are distributed as desired
            birads_balance = (0.2 * num_test < num_c1 < 0.3 * num_test and
                              0.2 * num_test < num_c2 < 0.3 * num_test and
                              0.2 * num_test < num_c3 < 0.3 * num_test and
                              0.2 * num_test < num_c4 < 0.3 * num_test)

            logger.info('\t\t\tClass balanced:\t\t%s' % class_balance)
            logger.info('\t\t\tTum size balance:\t%s' % tum_size_balance)
            logger.info('\t\t\tBI-RADS balance:\t%s' % birads_balance)
            logger.info('\t\t\tAdipose balance:\t%s' % adi_balance)

            # If the classes, tumor sizes, and BI-RADS classes are
            # balanced as expected, set flag to True
            test_conditions_satisfied = (class_balance and tum_size_balance
                                         and birads_balance and adi_balance)

    logger.info('\tTrain/test set split completed successfully with'
                ' random seed: %d' % rand_seed)

    if return_rand_seed:  # If returning the rand seed, also return it
        return (train_data, test_data, train_labels, test_labels,
                train_metadata, test_metadata, rand_seed)

    else:  # If not returning the rand seed, then don't
        return (train_data, test_data, train_labels, test_labels,
                train_metadata, test_metadata)
