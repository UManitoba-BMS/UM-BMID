% Tyson Reimer
% University of Manitoba
% October 16th, 2019

clear all;
close all;
clc;

%%  Define variables specifying which file to load

% The generation of data to use, must be in ['one', 'two']
gen = 'one';

% The type of data to use, must be in ['iczt', 'idft', 'fd']
% NOTE: 'iczt' is the type that is expected for the plot below
dataType = 'iczt';

% The type of sparams to use, must be in ['s11', 's21']
sparam = 's11';

% The reference calibration type to use, must be in ['emp', 'adi']
calType = 'emp';

%% Load the scan data to an array variable

% Get the file name to load
fileName = sprintf('%s_data_%s_%s.mat', dataType, sparam, calType);

% Get the path to the file's parent directory
fileDir = sprintf('datasets/gen-%s/clean/', gen);

% Get the path to the file 
filePath = fullfile(fileDir, fileName);

scanData = load(filePath);  % Load the data

% Extract the data array from the struct dtype it is stored in
scanDataFieldName = fieldnames(scanData);
scanData = getfield(scanData, scanDataFieldName{1});

%% Load the metadata to a variable

% Define the file name and full path to the metadata file
fileName = sprintf('md_list_%s_%s.mat', sparam, calType);
filePath = fullfile(fileDir, fileName);

metadata = load(filePath);  % Load the metadata

% Extract the metadata array from the struct dytpe it is stored in
metadataFieldName = fieldnames(metadata);
metadata = getfield(metadata, metadataFieldName{1});

%% Plot a sample sinogram - USE 'iczt' AS dataType FOR THIS

sampleIdx = 1;  % The index for the sample that will be plotted

% Take the abs-value and reshape for imshow
dataToPlot = abs(scanData(sampleIdx, :, :));
dataToPlot = reshape(dataToPlot, [size(dataToPlot, 2), ...
                                    size(dataToPlot, 3)]);

% Make the figure
figure;
imagesc(dataToPlot, 'y', linspace(0, 6, 1024));
title('Sample Sinogram');
xlabel('Antenna Position');
ylabel('Time of Response (ns)');
yticks(round(linspace(0, 6, 10), 3));
colorbar;

%% Print metadata content

% Get the metadata for this scan, extract it from struct dtype
thisMetadata = metadata{sampleIdx};
mdFieldNames = fieldnames(thisMetadata);

% For each info piece stored in the metadata
for mdIdx = 1 : length(mdFieldNames)
    
    % Get the value for this info piece for the sample scan
    infoVal = getfield(thisMetadata, mdFieldNames{mdIdx});
    infoStr = sprintf('%20s', mdFieldNames{mdIdx});
    
    if ~ isnan(infoVal)  % If the value was not NaN
        
        % Define the string that will be printed
        strToPrint = strcat(infoStr, '\t', string(infoVal));
        
    else  % If the value was NaN
        strToPrint = strcat(infoStr, '\t', 'NaN');
    end
    fprintf(strcat(strToPrint, '\n'));
end
