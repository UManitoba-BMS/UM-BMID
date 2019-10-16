% Tyson Reimer
% University of Manitoba
% September 5th, 2019


classdef LogisticRegression<handle
    % Logistic regression model for binary classification
    
    properties
        
        nFeatures  % The number of features of the samples
        params  % The model parameters
        
    end  % End for properties declarations
    
    methods
        
        function obj = LogisticRegression(nFeatures)
            % Init the class LogisticRegression
            %
            % Parameters
            % ----------
            % nFeatures : int
            %   The number of features used when fitting the model
            
            obj.nFeatures = nFeatures;  % Require nFeatures as input
            
            % Init model parameters to be small random values
            obj.params = rand([nFeatures + 1, 1]) - 0.5;
            
        end  % End for init function definition
                
        function probPreds = predictProba(obj, features)
            % Predict the scores for each sample 
            %
            % Parameters
            % ----------
            % features : array
            %   The features for each sample 
            %
            % Returns
            % -------
            % probPreds : array
            %   The predicted probabilities / scores for each sample
            
            % Concatenate the unity feature vector
            features = obj.reshapeFeatures(features);

            % Compute the logistic regression scores
            probPreds = 1 ./ (1 + exp(-features * obj.params));            
            
        end  % End for predictProba function definition
        
        function predLabels = predictLabels(obj, features)
            % Predict the class labels for each sample 
            % 
            % Parameters
            % ----------
            % features : array
            %   The features of each sample
            %
            % Returns
            % -------
            % predLabels : array
            %   The predicted binary class labels for each sample
            
            % Round the predicted scores to obtain the predicted labels
            predLabels = round(obj.predictProba(features));
            
        end  % End for predLabels function definition
        
        function obj = fit(obj, features, labels, learnRate, ...
                                maxIter)
            % Train the model to learn the model parameters
            %
            % Parameters
            % ----------
            % features : array
            %   The features of each sample
            % labels : array
            %   The binary class labels of each sample
            % learnRate : float
            %   The learning rate used for gradient descent
            % maxIter : int
            %   The maximum number of iterations used during training
            %
            % Returns
            % -------
            % costs : array
            %   The value of the cost function at each iteration 
            %   during training
            
            % Set default value of learning rate
            if ~exist('learnRate', 'var')
                learnRate = 0.01;
            end  % End if statement for learnRate existing
            
            % Set default value of maxIter
            if ~exist('maxIter', 'var')
                maxIter = 10000;
            end  % End if statement for maxIter existing
           
            nSamples = size(features, 1);  % Number of samples in set
            nIter = 0;  % Init the number of iterations performed
                                    
            % While the stopping criteria is not satisfied
            while nIter < maxIter
                
                nIter = nIter + 1;  % Increment iter counter
                
                % Get predicted scores
                preds = obj.predictProba(features);
                
                % Remove values that cause errors when passed through
                % the log() func
                preds(preds == 0) = 1e-5;
                preds(preds == 1) = 1 - 1e-5;
                
                % Copmute the gradient of the cost function with 
                % respect to each parameter
                paramGrad = obj.paramGrad(features, labels, preds, ...
                                            nSamples);
                                        
                % Update the model parameters using gradient descent
                obj.params = obj.params - learnRate * paramGrad;
                
            end  % End while loop over gradient descent training
            
        end  % End fit function definition
        
    end  % End methods declarations
    
    % Define private methods
    methods (Access = private)
        
        function features = reshapeFeatures(~, features)
            % Concatenates the unity feature vector to the features
            % 
            % Parameters
            % ----------
            % features : array
            %   The features for each sample
            %
            % Returns
            % -------
            % features : array
            %   Features for each sample, concatenated with unity 
            %   feature vector
            
            nSamples = size(features, 1);  % Number of samples
            
            % Concatenate unity feature vector
            features = [features, ones([nSamples, 1])];
            
        end  % End reshapeFeatures function definition       
        
        function grad = paramGrad(obj, features, labels, preds, ...
                                    nSamples)
            % Gradient of cost func with respect to each model param
            %
            % Parameters
            % ----------
            % features : array
            %   The features for each sample
            % labels : array
            %   The binary class labels (0s and 1s) for each sample
            % preds : array
            %   The predicted scores for each sample
            % nSamples : array
            %   The number of samples in the dataset
            %
            % Returns
            % -------
            % grad : array
            %   The gradient of the cost function with respect to each
            %   model parameter
            
            % Concatenate the unity feature vector
            features = obj.reshapeFeatures(features);
            
            % Compute the gradient with respect to each parameter            
            grad = ((1 / nSamples) * sum((preds - labels') .* ...
                                            features))';
            
        end  % End paramGrad function definition
    end  % End private methods declarations
    
end  % End LogisticRegression class definition