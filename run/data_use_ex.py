"""
Tyson Reimer
University of Manitoba
October 16th, 2019
"""

import os
import numpy as np
import matplotlib.pyplot as plt

from umbmid import get_proj_path, verify_path, get_script_logger
from umbmid.loadsave import load_pickle
from umbmid.content import report_metadata_content

###############################################################################

__DATA_DIR = os.path.join(get_proj_path(), 'datasets')
__OUTPUT_DIR = os.path.join(get_proj_path(), 'output/figs/')
verify_path(__OUTPUT_DIR)

###############################################################################

# Define the generation of data
gen = 'one'

# Define the type of data, must be in ['iczt', 'idft', 'fd']
# NOTE: for plotting the sinogram, 'iczt' is expected
data_type = 'iczt'

# Define the type of s-params to plot, must be in ['s11', 's21']
sparam = 's11'

# Define the type of reference calibration performed, must
# be in ['emp', 'adi']
cal_type = 'emp'

###############################################################################

# Define the data directory for this generation
this_data_dir = os.path.join(__DATA_DIR, 'gen-%s/clean/' % gen)

# Load the scan data
scan_data = load_pickle(os.path.join(this_data_dir, '%s_data_%s_%s.pickle'
                                     % (data_type, sparam, cal_type)))

###############################################################################

# Load the metadata
metadata = load_pickle(os.path.join(this_data_dir, 'md_list_%s_%s.pickle'
                                    % (sparam, cal_type)))

logger = get_script_logger(__file__)

report_metadata_content(metadata, logger)

###############################################################################

# The index for the scan that will be plotted
sample_idx = 0

# Take the abs-value and get the data that will be plotted
data_to_plot = np.abs(scan_data[0, :, :])

# Plot the data
plt.figure()
plt.imshow(data_to_plot, cmap='inferno', aspect='auto')
plt.title('Sample Sinogram')
plt.xlabel('Antenna Position')
plt.ylabel('Time of Response (ns)')
plt.yticks(np.round(np.linspace(0, 1024, 10)),
           ['%.2f' % ii for ii in np.linspace(0, 6, 10)])
plt.colorbar()
plt.show()

# Save the figure, can comment-out to not-save
plt.savefig(os.path.join(__OUTPUT_DIR, 'PythonExampleSinogram.png'),
            dpi=300)

###############################################################################

# Define the metadata for this experiment
this_md = metadata[sample_idx]

for info_key in this_md.keys():  # For each piece of info in metadata

    # Print the value for this piece of metadata
    print('%20s:\t%s' % (info_key, this_md[info_key]))
