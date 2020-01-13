"""
Tyson Reimer
University of Manitoba
July 19th, 2019
"""

import numpy as np

from umbmid import null_logger
from umbmid.build import get_info_piece_list

###############################################################################


def get_class_labels(metadata):
    """Get binary (tumor vs no-tumor) class labels for each sample

    Returns a list containing the class labels of each sample whose
    metadata is contained in the list metadata - label is 1 if the
    sample is tumor-containing, label is 0 if the sample did not
    contain a tumor.

    Parameters
    ----------
    metadata : list
        List containing the metadata dict for each sample

    Returns
    -------
    labels : array_like
        The binary labels (0 or 1) of the classes for each sample
    """

    labels = []  # Init array to return

    for sample_idx in range(len(metadata)):  # For each sample

        # If the tumor size was a number (indicating a tumor was
        # contained in the scan)
        if not np.isnan(metadata[sample_idx]['tum_rad']):

            # Assign a label of one to indicate the positive class
            labels.append(1)

        # If the tumor size was np.NaN (indicating that no tumor was
        # contained in the scan)
        else:

            # Assign a label of zero to indicate the negative class
            labels.append(0)

    return np.array(labels)


def get_adipose_shell_ids(metadata):
    """Return list of the adipose shell ID for each sample

    Returns a list containing the adipose shell IDs (ex: A1, A2, etc.)
    of each sample whose metadata is contained in the list metadata

    Parameters
    ----------
    metadata : list
        List containing the metadata dict for each sample

    Returns
    -------
    adipose_ids : array_like
        Vector containing the adipose shell IDs of each sample
    """

    # Get the full phantom IDs (ex: 'A2F4')
    phantom_ids = get_info_piece_list(metadata, 'phant_id')

    # Get only the first two characters of the full ID
    adipose_ids = [phantom_id[:2] for phantom_id in phantom_ids]

    return np.array(adipose_ids)


def report_metadata_content(metadata, logger=null_logger):
    """Report major metadata info to a logger

    Reports the BI-RADS class, tumor size, and adipose-id
    distributions for all samples whose metadata is in the metadata
    list, and for only positive samples, and only negative samples.

    Parameters
    ----------
    metadata : list
        List containing the metadata dict for each sample
    logger : logging_object
        A logging object
    """

    num_samples = len(metadata)  # Find the total number of samples

    # Get the BIRADS classes, tumor sizes, adipose shell IDs, and class
    # labels
    birads = get_info_piece_list(metadata, 'birads')
    tum_sizes = get_info_piece_list(metadata, 'tum_rad')
    adipose_ids = get_adipose_shell_ids(metadata)
    labels = get_class_labels(metadata)

    # Get the number of positive and negative samples
    num_pos, num_neg = int(np.sum(labels)), int(np.sum(1 - labels))

    num_c1, num_c2, num_c3, num_c4 = (int(np.sum(birads == 1)),
                                      int(np.sum(birads == 2)),
                                      int(np.sum(birads == 3)),
                                      int(np.sum(birads == 4)))

    # Init dict for storing the adipose shell IDs
    adi_shell_nums = dict()

    # For each unique adi shell ID
    for adi_shell in np.unique(adipose_ids):

        # Find how many samples had this adi_shell ID
        adi_shell_nums[adi_shell] = int(np.sum(adipose_ids == adi_shell))

    tum_size_nums = dict()  # Init dict for storing the tumor sizes

    for tum_size in np.unique(tum_sizes):  # For each unique tumor size

        # If this unique 'tumor size' is a num
        if not np.isnan(tum_size):

            # Find how many samples had this tumor size
            tum_size_nums['%d cm' % tum_size] = int(np.sum(tum_sizes ==
                                                           tum_size))

    # Print the overall metadata of interest to the console
    logger.info('')
    logger.info('\tOverall positive samples:\t%d\t|\t%.2f%%' %
                (num_pos, 100 * num_pos / num_samples))
    logger.info('\tOverall negative samples:\t%d\t|\t%.2f%%' %
                (num_neg, 100 * num_neg / num_samples))
    logger.info('')

    logger.info('\tOverall Class I samples:\t%d\t|\t%.2f%%' %
                (num_c1, 100 * num_c1 / num_samples))
    logger.info('\tOverall Class II samples:\t%d\t|\t%.2f%%' %
                (num_c2, 100 * num_c2 / num_samples))
    logger.info('\tOverall Class III samples:\t%d\t|\t%.2f%%' %
                (num_c3, 100 * num_c3 / num_samples))
    logger.info('\tOverall Class IV samples:\t%d\t|\t%.2f%%' %
                (num_c4, 100 * num_c4 / num_samples))

    logger.info('')

    for tum_size in tum_size_nums.keys():
        logger.info('\tOverall %s tumors:\t%d\t|\t%.2f%%' %
                    (tum_size, tum_size_nums[tum_size],
                     100 * tum_size_nums[tum_size] / num_pos))

    logger.info('')
    for adi_shell in adi_shell_nums.keys():
        logger.info('\tOverall %s samples:\t%d\t|\t%.2f%%' %
                    (adi_shell, adi_shell_nums[adi_shell],
                     100 * adi_shell_nums[adi_shell] / num_samples))

    # Find the BI-RADS classes for the positive samples
    pos_c1s = int(np.sum(np.logical_and(birads == 1, labels == 1)))
    pos_c2s = int(np.sum(np.logical_and(birads == 2, labels == 1)))
    pos_c3s = int(np.sum(np.logical_and(birads == 3, labels == 1)))
    pos_c4s = int(np.sum(np.logical_and(birads == 4, labels == 1)))

    # Init dict for the positive adi_shell IDs
    pos_adi_shell_nums = dict()
    for adi_shell in np.unique(adipose_ids):

        # Find the number of positive samples with this adi_shell ID
        pos_adi_shell_nums[adi_shell] = \
            int(np.sum(np.logical_and(adipose_ids == adi_shell, labels == 1)))

    logger.info('')
    logger.info('\tFor positive samples...')

    logger.info('')
    logger.info('\t\tClass I samples:\t%d\t|\t%.2f%%' %
                (pos_c1s, 100 * pos_c1s / num_pos))
    logger.info('\t\tClass II samples:\t%d\t|\t%.2f%%' %
                (pos_c2s, 100 * pos_c2s / num_pos))
    logger.info('\t\tClass III samples:\t%d\t|\t%.2f%%' %
                (pos_c3s, 100 * pos_c3s / num_pos))
    logger.info('\t\tClass IV samples:\t%d\t|\t%.2f%%' %
                (pos_c4s, 100 * pos_c4s / num_pos))

    logger.info('')
    for adi_shell in pos_adi_shell_nums.keys():
        logger.info('\t\tOverall %s samples:\t%d\t|\t%.2f%%' %
                    (adi_shell, pos_adi_shell_nums[adi_shell],
                     100 * pos_adi_shell_nums[adi_shell] / num_pos))

    # Find the BI-RADS classes for the negative samples
    neg_c2s = int(np.sum(np.logical_and(birads == 2, labels == 0)))
    neg_c3s = int(np.sum(np.logical_and(birads == 3, labels == 0)))
    neg_c1s = int(np.sum(np.logical_and(birads == 1, labels == 0)))
    neg_c4s = int(np.sum(np.logical_and(birads == 4, labels == 0)))

    # Init dict for the negative adi_shell IDs
    neg_adi_shell_nums = dict()
    for adi_shell in np.unique(adipose_ids):

        # Find the number of negative samples with this adi_shell ID
        neg_adi_shell_nums[adi_shell] = \
            int(np.sum(np.logical_and(adipose_ids == adi_shell, labels == 0)))

    logger.info('')
    logger.info('\tFor negative samples...')

    logger.info('')
    logger.info('\t\tClass I samples:\t%d\t|\t%.2f%%' %
                (neg_c1s, 100 * neg_c1s / num_neg))
    logger.info('\t\tClass II samples:\t%d\t|\t%.2f%%' %
                (neg_c2s, 100 * neg_c2s / num_neg))
    logger.info('\t\tClass III samples:\t%d\t|\t%.2f%%' %
                (neg_c3s, 100 * neg_c3s / num_neg))
    logger.info('\t\tClass IV samples:\t%d\t|\t%.2f%%' %
                (neg_c4s, 100 * neg_c4s / num_neg))

    logger.info('')
    for adi_shell in neg_adi_shell_nums.keys():
        logger.info('\t\tOverall %s samples:\t%d\t|\t%.2f%%' %
                    (adi_shell, neg_adi_shell_nums[adi_shell],
                     100 * neg_adi_shell_nums[adi_shell] / num_neg))
