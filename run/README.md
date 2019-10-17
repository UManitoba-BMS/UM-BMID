# UM-BMID Run

This folder contains scripts that are meant to be executed. They import 
functions from the `/modules/` folder. 

## Using the Dataset

The file `/run/data_use_ex.py` and `/run/dataUseEx.m` demonstrate how to 
import the dataset using the clean `.pickle` and `.mat` files. 

These files demonstrate:

- How to load the clean files
- How to plot the measured responses from one scan
- How to access the metadata from one scan

## _Make_ Files

The file `/run/make_figs.py` was used to make the figure in the 
EuCAP 2020 paper presenting UM-BMID.

The file `/run/make_traintest.py` was used to make the training and 
testing datasets that were used to produce the results in the EuCAP 2020 
paper.

The file `/run/make_clean_files.py` was used to make the clean data 
`.pickle` and `.mat` files that are hosted at https://bit.ly/UM-bmid. 

## Others

The `/run/logreg_analysis.py` file was used to train the logistic
regression classifier that was used to produce the results in the 
EuCAP 2020 paper.  
