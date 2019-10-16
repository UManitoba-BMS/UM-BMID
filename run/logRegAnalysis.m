% Tyson Reimer
% University of Manitoba
% October 16th, 2019

%% Define training parameters

clear all;
close all;
clc;

learnRate = 1;
maxIter = 10000;

%% Load data and labels

% Load train, test data
trainData = load('datasets/gen-one/clean/train_data.mat');
trainData = trainData.train_data;
testData = load('datasets/gen-one/clean/test_data.mat');
testData = testData.test_data;

% Load train, test labels
trainLabels = load('datasets/gen-one/clean/train_labels.mat');
trainLabels = trainLabels.train_labels;
trainLabels = cast(trainLabels, 'double');
testLabels = load('datasets/gen-one/clean/test_labels.mat');
testLabels = testLabels.test_labels;
testLabels = cast(testLabels, 'double');


%% Preprocess data

% Convert the training data to the time-domain
for sampleIdx = 1 : size(trainData, 1)
   trainData(sampleIdx, :, :) = ifft(trainData(sampleIdx, :, :)); 
end

% Convert the test data to the time-domain
for sampleIdx = 1 : size(testData, 1)
   testData(sampleIdx, :, :) = ifft(testData(sampleIdx, :, :)); 
end

% Take the abs-value of the complex time-domain signals
trainData = abs(trainData(:, 6:40, :));
testData = abs(testData(:, 6:40, :));

% Scale each training sample to have unity maximum value
for sampleIdx = 1 : size(trainData, 1)
   dataHere = trainData(sampleIdx, :, :);
   maxVal = max(dataHere(:));
   trainData(sampleIdx, :, :) = trainData(sampleIdx, :, :) / maxVal;
end

% Scale each test sample to have unity maximum value
for sampleIdx = 1 : size(testData, 1)
   dataHere = testData(sampleIdx, :, :);
   maxVal = max(dataHere(:));
   testData(sampleIdx, :, :) = testData(sampleIdx, :, :) / maxVal;
end

% Flatten feature vectors
trainData = reshape(trainData, ...
                    [size(trainData, 1), size(trainData, 2) ...
                    * size(trainData, 3)]);
testData = reshape(testData, ...
                    [size(testData, 1), size(testData, 2) ...
                    * size(testData, 3)]);                

%%

nRuns = 10;  % Number of runs over which performance will be averaged

% Init arrays for storing results
testAccs = zeros([nRuns, 1]);
testSens = zeros([nRuns, 1]);
testSpec = zeros([nRuns, 1]);

for runIdx = 1 : nRuns  % For each run
    
    fprintf('Working on run [%3d / %3d]...\n\n', runIdx, nRuns);
    
    % Init the logistic regression model
    logReg = LogisticRegression(size(trainData, 2));
    
    % Fit the model using the training data
    logReg.fit(trainData, trainLabels, learnRate, maxIter);
    
    bestAcc = 0;  % Init value for the best accuracy on train set
    
    % Get the predicted scores for each training sample
    trainPreds = logReg.predictProba(trainData);
    
    % Define possible decision thresholds
    thresholds = linspace(0, 1, 1000);  
    
    for thresIdx = 1 : length(thresholds)  % Loop over thresholds
        
        thresh = thresholds(thresIdx);
        
        % Get the true/false positives/negatives here
        tp = sum(trainLabels == 1 & trainPreds' > thresh);
        tn = sum(trainLabels == 0 & trainPreds' < thresh);
        fp = sum(trainLabels == 0 & trainPreds' > thresh);
        fn = sum(trainLabels == 1 & trainPreds' < thresh);
        
        % Determine the training accuracy at this threhsold
        trainAcc = (tp + tn) / (tp + tn + fp + fn);
        
        if trainAcc > bestAcc  % If this is the best accuracy yet
            
            bestAcc = trainAcc;  % Set best accuracy to this value
            bestThresh = thresh;  % Store the best decision threshold
        end  
    end
    
    % Predict scores on test set
    testPreds = logReg.predictProba(testData);
    
    % Find the true/false positives/negatives for the test set
    tp = sum(testLabels == 1 & testPreds' > bestThresh);
    tn = sum(testLabels == 0 & testPreds' < bestThresh);
    fp = sum(testLabels == 0 & testPreds' > bestThresh);
    fn = sum(testLabels == 1 & testPreds' < bestThresh);
    
    % Find the accuracy, sensitivity, and specificity on test set
    acc = (tp + tn) / (tp + tn + fp + fn);
    sens = tp / (tp + fn);
    spec = tn / (tn + fp);
    
    fprintf('Accuracy:\t\t\t%.4f\n', acc);
    fprintf('Sensitivity:\t\t%.4f\n', sens);
    fprintf('Specificity:\t\t%.4f\n', spec);
    
    % Store metrics
    testAccs(runIdx) = acc;
    testSens(runIdx) = sens;
    testSpec(runIdx) = spec;
       
end

% Report averages
fprintf('Final results:\n');
fprintf('Accuracy:\t\t\t%.4f +/- %.4f\n', mean(testAccs), std(testAccs));
fprintf('Sensitivity:\t\t%.4f +/- %.4f\n', mean(testSens), ...
                                            std(testSens));
fprintf('Specificity:\t\t%.4f +/- %.4f\n', mean(testSpec), ...
                                            std(testSpec));
                            
                            