# UM-BMID

The University of Manitoba Breast Microwave Imaging Dataset (UM-BMID) is
an open-access dataset available to all researchers. The dataset contains
data from experimental scans of MRI-derived breast phantoms.

**The dataset itself can be found [here](https://bit.ly/UM-bmid).** 
The shortened link is https://bit.ly/UM-bmid (case sensitive). 

The dataset is described in an accepted manuscript:

T. Reimer, J. Krenkevich, and S. Pistorius, "An open-access experimental
dataset for breast microwave imaging,", _2020 European Conference on
Antennas and Propagation (EuCAP 2020)_, accepted.

This GitHub repository contains the code used to produce the results
presented in that paper and supportive scripts for the UM-BMID dataset.

## Getting Started

### Accessing and Downloading UM-BMID

The dataset itself (and accompanying documentation) can be found 
[here](https://bit.ly/UM-bmid) (https://bit.ly/UM-bmid, case sensitive).

Rather than downloading the entire dataset, we recommend finding individual
files that interest you, and only downloading those specific files (due to the
size of the dataset). The file `/docs/UM-BMID_README.txt` (found
[here](https://github.com/UManitoba-BMS/UM-BMID/blob/master/docs/UM-BMID_README.txt))
 describes the folder structure of the Google Drive and contains information
about the individual data files.

### Prerequisites

This repository contains both Python and Matlab/Octave files. The Python
 requirements are: 

- Python 3.6 (or more recent) 

- Libraries in the `requirements.txt` file

  - numpy  >= 1.16.2
  - pathlib >= 1.0.1
  - scipy >= 1.2.1
  - matplotlib >= 3.0.3
  
The Matlab/Octave requirements are:

- Matlab 2017a (or more recent) 

### Installing

We recommend using the Anaconda distribution for Python 3.x, which can be
 downloaded [here](https://www.anaconda.com/distribution/).
 
After installing a Python distribution, the required libraries can be
installed via the command line. After navigating to the project directory, 
enter the command:
 
```
pip install -r requirements.txt
```

This will install all the libraries listed in the `requirements.txt` file.


## Usage

### Running the Tests

The `UM-BMID/tests/` folder contains two Python test files and one 
Matlab/Octave test file. 

- The `/tests/check_requirements.py` file checks if the required libraries
 are installed.
 
- The `/tests/dataset_test.py` and `/tests/datsetTest.m` files check if the
 dataset files from 
[here](https://bit.ly/UM-bmid) have been placed in the `/datasets/` folder
in the project. 

### Exploring the Dataset

The best way to explore the dataset is to download the following files:

- `UM-BMID/scan-data/gen-{one, two}/clean/idft_data_s11_emp.{mat, pickle}`
- `UM-BMID/scan-data/gen-{one, two}/clean/md_list_s11_emp.{mat, pickle}`

The first file contains the measured frequency-domain S<sub>11</sub> parameters
of all scans in that generation of the dataset, after having performed 
empty-chamber reference subtraction. The second file contains the metadata
for each of these scans.

Alternatively, to use data **without** any reference-subtraction, 
download the files:

- `UM-BMID/scan-data/gen-{one, two}/simple-clean/{python, matlab}-data/fd_data_gen_{one, two}_s11.{pickle, mat}`
- `UM-BMID/scan-data/gen-{one, two}/simple-clean/{python, matlab}-data/metadata_gen_{one, two}.{pickle, mat}`

These files contain the frequency-domain S<sub>11</sub> parameters of all scans,
including empty-chamber reference scans. 

### Data Use Examples

An example demonstrating usage of the simple-data files is described here. 
To begin, download the files:

- `UM-BMID/scan-data/gen-two/simple-clean/python-data/fd_data_gen_two_s11.pickle`
- `UM-BMID/scan-data/gen-two/simple-clean/python-data/metadata_gen_two.pickle`

and place them in your local UM-BMID repository under the folder:

- `UM-BMID/scan-data/gen-two/simple-clean/python-data/`

After downloading the files and placing them in the folder in your local
UM-BMID project directory, use the `../run/simple_data_use_ex.py` file to
explore loading and using the dataset corresponding metadata.

Two sample files for using the **clean** dataset files are contained
in the `/run/` folder: the `/run/dataUseEx.m` and `/run/data_use_ex.py` files.
These files demonstrate how to import the clean dataset files, display
the sinogram measured from an experimental scan, and access the metadata for
that experimental scan.

More information can be found in the `README.md` within the `/run/` folder.  


## Contributing

Please read the CONTRIBUTING.md for details on contributing to the project.

## Authors

- Tyson Reimer, University of Manitoba, Department of Physics
 & Astronomy, Winnipeg, Manitoba
- Jordan Krenkevich, University of Manitoba, Department of Physics
 & Astronomy, Winnipeg, Manitoba
- Dr. Stephen Pistorius, University of Manitoba, Department of Physics
 & Astronomy, Winnipeg, Manitoba

## License

This project is licensed under the Apache 2.0 License. See the `LICENSE` file
 for more information.

## Acknowledgments

The authors would like to thank Masoud Kamely and Hillary Kroeker for their
assistance in performing some of the experimental scans for UM-BMID. The
authors would also like to thank Jorge Sacristan for many valuable
discussions.


