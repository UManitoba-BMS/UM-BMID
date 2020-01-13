"""
Tyson Reimer
University of Manitoba
September 4th, 2019
"""

import numpy as np

###############################################################################


class LogisticRegression:
    """Logistic regression model for binary classification"""

    def __init__(self, n_features):
        """Init class LogisticRegression

        Parameters
        ----------
        n_features : int
            The number of features that will be used when fitting the
            model
        """

        self.n_features = n_features   # Set the number of features

        # Init the model parameters to small, random values
        # self.params = np.random.random([n_features + 1, ]) * 0.1 - 0.05

        self.params = np.random.random([n_features + 1, ]) - 0.5

    def _param_grad(self, features, labels, preds, n_samples):
        """Get the gradient of the cost func with respect to each param

        Parameters
        ----------
        features : array_like
            The features for each sample used during training
        labels : array_like
            Binary class labels (0s and 1s) for each sample
        preds : array_like
            The predicted probabilities for each sample
        n_samples : int
            The number of samples used during training

        Returns
        -------
        param_grad : array_like
            The gradient of the cost function with respect to each param
        """

        features = self._reshape_features(features)  # Reshape features

        # Find the gradient with respect to each parameter
        param_grad = (1 / n_samples) * np.sum((preds - labels)[:, None] *
                                              features, axis=0)

        return param_grad

    @staticmethod
    def _reshape_features(features):
        """Reshapes features by concatenating unity feature

        Parameters
        ----------
        features : array_like
            The features that will be reshaped

        Returns
        -------
        features : array_like
            The features, with a vector of unity feature concatenated
            at the end
        """

        # Find the number of samples
        n_samples = np.size(features, axis=0)

        # Concatenate the unity feature vector
        features = np.append(features, np.ones([n_samples, ])[:, None], axis=1)

        return features

    def predict_proba(self, features):
        """Predict the scores for each sample in the features arr

        Parameters
        ----------
        features : array_like
            The features for each sample

        Returns
        -------
        prob_preds : array_like
            The predicted logistic regression scores for each sample
            in the features array
        """

        # Reshape the features to concatenate unity feature vector
        features = self._reshape_features(features)

        # Use the sigmoid function
        prob_preds = 1 / (1 + np.exp(-features @ self.params))

        return prob_preds

    def predict_labels(self, features):
        """Predict the class labels for each sample in the features arr

        Parameters
        ----------
        features : array_like
            The features for each sample

        Returns
        -------
        label-preds : array_like
            The predicted class labels for each sample in the features
            array
        """

        # Round the predicted probabilities to obtain the predicted
        # classes
        label_preds = np.round(self.predict_proba(features)).astype(int)

        return label_preds

    def fit(self, features, labels, learn_rate=0.01, max_iter=10000):
        """Train (grad descent) the model to learn the model parameters

        Parameters
        ----------
        features : array_like
            The features for each sample
        labels : array_like
            The binary class labels (0s or 1s)
        learn_rate : float
            The learning rate used for gradient descent
        max_iter : int
            The maximum number of iterations before termination of the
            optimization routine
        """

        # Find the number of samples used for training
        n_samples = np.size(features, axis=0)

        # Init stopping-criteria parameters
        cost_change = 1e9
        threshold = 1e-5
        n_iter = 0

        # Init list for storing value of cost func at each iteration
        costs = []

        # While stopping criteria is not satisfied
        while cost_change > threshold and n_iter < max_iter:

            n_iter += 1  # Increment iteration number counter

            # Predict the scores for each sample
            preds = self.predict_proba(features)

            # Prevent crashes by removing not-acceptable values
            preds[preds == 0] = 1e-5
            preds[preds == 1] = 1 - 1e-5

            # Get the gradient of the cost function with respect to
            # each parameter
            param_grad = self._param_grad(features, labels, preds, n_samples)

            # Update the parameters using gradient descent
            self.params -= learn_rate * param_grad

            # Find the value of the cost function at this iteration
            cost = (1 / n_samples) * np.sum(-labels * np.log(preds)
                                            - (1 - labels) * np.log(1 - preds))

            # Store the cost function from this iteration
            costs.append(cost)
