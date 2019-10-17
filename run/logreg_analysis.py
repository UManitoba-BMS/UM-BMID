"""
Tyson Reimer
University of Manitoba
September 14th, 2019
"""

import os
import numpy as np
from sklearn.metrics import roc_auc_score

from modules import get_proj_path, get_script_logger
from modules.loadsave import load_pickle
from modules.ai.logreg import LogisticRegression
from modules.ai.preprocessing import normalize_samples

###############################################################################

__DATA_DIR = os.path.join(get_proj_path(), 'datasets/gen-one/clean/')

__LEARN_RATE = 1  # Set the learning rate for gradient descent
__MAX_ITER = 10000  # Set the number of iterations used to train

###############################################################################

# Load the training data, labels, and metadata
train_data = load_pickle(os.path.join(__DATA_DIR,
                                      'train_data.pickle'))
train_labels = load_pickle(os.path.join(__DATA_DIR,
                                        'train_labels.pickle'))
train_md = load_pickle(os.path.join(__DATA_DIR,
                                    'train_md.pickle'))

# Load the test data, labels, and metadata
test_data = load_pickle(os.path.join(__DATA_DIR,
                                     'test_data.pickle'))
test_labels = load_pickle(os.path.join(__DATA_DIR,
                                       'test_labels.pickle'))
test_md = load_pickle(os.path.join(__DATA_DIR,
                                   'test_md.pickle'))

###############################################################################

# Convert each train sample from the frequency-domain to the time-domain
for sample_idx in range(np.size(train_data, axis=0)):
    train_data[sample_idx, :, :] = np.fft.ifft(train_data[sample_idx, :, :],
                                               axis=0)
# Convert each test sample from the frequency-domain to the time-domain
for sample_idx in range(np.size(test_data, axis=0)):
    test_data[sample_idx, :, :] = np.fft.ifft(test_data[sample_idx, :, :],
                                              axis=0)

# Take the abs-value of ecah sample, and apply the time-domain window
train_data = np.abs(train_data[:, 5:40, :])
test_data = np.abs(test_data[:, 5:40, :])

# Normalize each sample to have a maximum of unity
train_data = normalize_samples(train_data)
test_data = normalize_samples(test_data)

# Flatten the feature arrays of each sample to be a 1D feature vector
train_data = np.reshape(train_data, [np.size(train_data, axis=0), 35 * 72])
test_data = np.reshape(test_data, [np.size(test_data, axis=0), 35 * 72])

###############################################################################


def get_best_acc(labels, preds, fixed_threshold=-1.0):
    """Finds the best threshold, acc, sens and spec for a classifier

    Parameters
    ----------
    labels : list, array_like
        The binary class labels of each sample
    preds : list, array_like
        The predicted scores of each sample
    fixed_threshold : float
        If set to -1.0, will not use a fixed threshold. If set to any
        other value, will find the acc/sens/spec at that threshold

    Returns
    -------
    best_threshold : float
        The threshold that results in the highest diagnostic accuracy,
        if fixed_threshold == -1.0, otherwise is fixed_threshold
    best_acc : float
        The best diagnostic accuracy
    best_sens : float
        The best sensitivity
    best_spec : float
        The best specificity
    """

    labels = np.array(labels)  # Convert to np array
    preds = np.array(preds)  # Convert to np array

    # Init the best acc/sens/spec/threshold
    best_acc = -1
    best_sens = -1
    best_spec = -1
    best_threshold = 0

    if fixed_threshold == -1.0:  # If fixed_threshold at default value

        # Define var for possible thresholds
        possible_thresholds = np.linspace(0, 1, 1000)

    else:  # If fixed_threshold specified to be not-default
        assert 0 <= fixed_threshold <= 1, \
                "Error: fixed_threshold must be between 0 and 1"

        # Set possible thresholds to be list of only this threshold
        possible_thresholds = [fixed_threshold]

    for thresh in possible_thresholds:  # For each threshold

        # Find the true positives/negatives, false postives/negatives
        tp = np.sum(np.logical_and(labels == 1, preds > thresh))
        tn = np.sum(np.logical_and(labels == 0, preds < thresh))
        fn = np.sum(np.logical_and(labels == 1, preds < thresh))
        fp = np.sum(np.logical_and(labels == 0, preds > thresh))

        # Get the accuracy/sensitivity/specificity at this threshold
        acc = (tp + tn) / (fn + fp + tn + tp)
        sens = tp / (tp + fn)
        spec = tn / (tn + fp)

        if acc > best_acc:  # If this is the best accuracy thus far

            # Store the acc/sens/spec/threshold as the *best*
            best_acc = acc
            best_threshold = thresh
            best_sens = sens
            best_spec = spec

    logger.info('\tbest threshold:\t%.3f' % best_threshold)

    return best_threshold, best_acc, best_sens, best_spec


def report_results(data, labels, return_threshold=False, threshold=-1.0):
    """Reports the classification results to the logger

    Parameters
    ----------
    data : array_like
        The features for each sample in the data
    labels : list, array_like
        The binary class labels for each sample in the data
    return_threshold : bool
        If True, will also return the threshold used to compute the
        classification results
    threshold : float
        If -1.0, will find the best threshold and use that to find
        classification results. Otherwise, will use its value to find
        classification results.

    Returns
    -------
    threshold : float
        The threshold - only returned if return_threshold
    acc : float
        The accuracy of the classification predictions
    roc_score : float
        The ROC AUC score of the classification predictions
    sens : float
        The sensitivity of the classification predictions
    spec : float
        The specificity of the classification predictions
    """

    # Get the predicted scores for each sample
    pred_probs = logreg.predict_proba(data)

    # Find the threshold, acc/sens/spec for these predictions
    threshold, acc, sens, spec = get_best_acc(labels, pred_probs,
                                              fixed_threshold=threshold)

    # Compute the ROC AUC score for the predictions
    roc_score = roc_auc_score(labels, pred_probs)

    # Report to the logger
    logger.info('\t\tAcc:\t%.3f' % acc)
    logger.info('\t\tROC:\t%.3f' % roc_score)
    logger.info('\t\tSens:\t%.3f' % sens)
    logger.info('\t\tSpec:\t%.3f' % spec)

    if return_threshold:  # If returning the threshold, then do that
        return threshold, acc, roc_score, sens, spec

    else:  # If not returning the threshold, then return metrics only
        return acc, roc_score, sens, spec


###############################################################################

if __name__ == '__main__':

    # Define the logger and output init statements
    logger = get_script_logger(__file__)
    logger.info('\tBEGINNING...')
    logger.info('\tMax Iter: %d\tLearn Rate: %.3f' % (__MAX_ITER,
                                                      __LEARN_RATE))

    # The number of runs over which results will be averaged
    n_runs = 100

    # Init lists for storing the metrics on the train/test sets at
    # each iteration
    train_acc, train_roc = [], []
    train_sens, train_spec = [], []
    test_acc, test_roc = [], []
    test_sens, test_spec = [], []

    for run_idx in range(n_runs):  # For each run

        logger.info('Working on run [%3d / %3d]' %
                    (run_idx + 1, n_runs))

        logger.info('\tTest Set NumPos: %d\tNumNeg: %d'
                    % (np.sum(test_labels), np.sum(1 - test_labels)))

        # Define the logistic regression classifier
        logreg = LogisticRegression(n_features=np.size(train_data, axis=1))

        # Fit the classifier
        logreg.fit(train_data, train_labels,
                   max_iter=__MAX_ITER,
                   learn_rate=__LEARN_RATE)

        # Get the results and threshold from the training set
        logger.info('\tTrain Data:')
        threshold, acc, roc, sens, spec = report_results(train_data,
                                                         train_labels,
                                                         return_threshold=True,
                                                         threshold=-1.0)

        # Store the metrics for the training set
        train_acc.append(acc)
        train_roc.append(roc)
        train_sens.append(sens)
        train_spec.append(spec)

        # Get the results on the test set using threshold from the
        # training set
        logger.info('\tTest Data:')
        acc, roc, sens, spec = report_results(test_data, test_labels,
                                              threshold=threshold)

        # Store the metrics for the test set
        test_acc.append(acc)
        test_roc.append(roc)
        test_sens.append(sens)
        test_spec.append(spec)

    # Convert the lists to np arrays
    train_acc = np.array(train_acc)
    train_roc = np.array(train_roc)
    test_acc = np.array(test_acc)
    test_roc = np.array(test_roc)
    test_sens = np.array(test_sens)
    test_spec = np.array(test_spec)

    # Report final results to logger
    logger.info('Train Final:')
    logger.info('Acc:\t%.3f +/- %.3f' %
                (np.mean(train_acc), np.std(train_acc)))
    logger.info('ROC:\t%.3f +/- %.3f' %
                (np.mean(train_roc), np.std(train_roc)))

    logger.info('Test  Final:')
    logger.info('Acc:\t%.6f +/- %.6f' %
                (np.mean(test_acc), np.std(test_acc)))
    logger.info('ROC:\t%.6f +/- %.6f' %
                (np.mean(test_roc), np.std(test_roc)))
    logger.info('Sens:\t%.6f +/- %.6f' %
                (np.mean(test_sens), np.std(test_sens)))
    logger.info('Spec:\t%.6f +/- %.6f' %
                (np.mean(test_spec), np.std(test_spec)))
