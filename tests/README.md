# UM-BMID Tests

The tests should be run **after** having placed the data files from 
[here](https://bit.ly/UM-bmid) in the `/datasets/` folder within your local
project.

## `check_requirements.py`

This test file will verify that the required Python libraries are installed
 on your local system. If any are missing, you can install them using
 
 ```
pip install <pkg-name>
```

or, if using Anaconda,

```
conda install <pkg-name>
```

## `dataset_test.py` and `datasetTest.m`

These files check if the folders and files from 
[here](https://bit.ly/UM-bmid) have been placed in the `/datasets/` folder
within the local project.

If any files are missing, you will be notified via the console.

You do not need _all_ data files. If you are working in Matlab/Octave, you 
only need to use the `.mat` files (and in Python you only need the `.pickle` 
files). 