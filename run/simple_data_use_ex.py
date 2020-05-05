"""
Tyson Reimer
University of Manitoba
October 22nd, 2019
"""

import os
import numpy as np
import matplotlib.pyplot as plt

from umbmid import get_proj_path, verify_path, get_script_logger
from umbmid.sigproc import iczt
from umbmid.loadsave import load_pickle

###############################################################################

# The generation of dataset to be explored - must be 'one' or 'two'
gen = 'two'

# The path to the data directory on your local PC
__DATA_DIR = os.path.join(get_proj_path(),
                          'datasets/gen-%s/simple-clean/python-data/'
                          % gen)

__OUTPUT_DIR = os.path.join(get_proj_path(),
                            'output/simple-use-ex-output/')
verify_path(__OUTPUT_DIR)

###############################################################################


def plot_td_sinogram(td_data, ini_t=0, fin_t=6e-9, title='', save_fig=False,
                     save_str='', transparent=False, dpi=300, cmap='inferno'):
    """Plots a time-domain sinogram

     Displays a sinogram in the time domain (transferred to the time domain
     via the ICZT).

     Parameters
     ----------
     td_data : array_like
         S-parameters in the time domain
     ini_t : float
         The initial time-point in the time-domain, in seconds
     fin_t : float
         The final time-point in the time-domain, in seconds
     title : str
         The title used for displaying the data
     save_fig : bool
         If true, will save the figure to a .png file - default is False
     save_str : str
         The title of the .png file to be saved if save_image is true -
         default is empty str, triggering the save_string to be set to
         the title
     transparent : bool
        If True, will save the figure with transparent=True, else will
        save with default white background
     dpi : int
         The DPI to use if saving the figure
     cmap : str
         The colormap that will be used to display the sinogram
     """

    td_data = np.abs(td_data)  # Take the abs-value of the complex vals

    n_time_pts = np.size(td_data, axis=0)  # Find number of time-pts

    # Find the vector of temporal points in the time domain used in the
    # scan
    scan_times = np.linspace(ini_t, fin_t, n_time_pts)

    # Declare the extent for the plot, along x-axis from antenna
    # position 1 to N, with N being the number of antenna positions used
    # in the scan, along y-axis from user specified points in
    # time-domain
    plot_extent = [1, 360, scan_times[-1] * 1e9, scan_times[0] * 1e9]

    # Determine the aspect ratio for the plot to make it have equal axes
    plot_aspect_ratio = 360 / (scan_times[-1] * 1e9)

    # Make the figure for displaying the reconstruction
    plt.figure()

    # Declare the default font for our figure to be Times New Roman
    plt.rc('font', family='Times New Roman')

    # Plot the sinogram
    plt.imshow(td_data, cmap=cmap, extent=plot_extent,
               aspect=plot_aspect_ratio)

    # Set the size for the x,y ticks and set which ticks to display
    plt.tick_params(labelsize=14)
    scan_times *= 1e9
    plt.gca().set_yticks([round(ii, 2)
                          for ii in scan_times[::n_time_pts // 8]])
    plt.gca().set_xticks([round(ii)
                          for ii in np.linspace(0, 360, 360)[::75]])

    # Create the colorbar and set the colorbar tick size, also set
    # the format specifier to be as entered by user - default is '%.3f'
    plt.colorbar(format='%.3f').ax.tick_params(labelsize=14)

    # Label the plot axes and assign the plot a title
    plt.title(title, fontsize=20)
    plt.xlabel('Rotational Position (' + r'$^\circ$' + ')', fontsize=16)
    plt.ylabel('Time of Response (ns)', fontsize=16)
    plt.tight_layout()

    # If the user set save_data to True, and therefore wanted to save
    # the figure as a png file
    if save_fig:

        # If the user did not specify a save string, then set the
        # save string to be the title string, without spaces
        if not save_str:
            # Define a string for saving the figure, replace any spaces
            # in the title with underscores
            save_str = title.replace(' ', '_') + '.png'

        # If the user did specify a save string, then add '.png' file
        # extension to it for saving purposes
        else:
            save_str += '.png'

        # Save the figure to a png file
        plt.savefig(save_str, transparent=transparent, dpi=dpi)

    else:  # If not saving the figure, then show the figure
        plt.show()

###############################################################################


if __name__ == '__main__':

    logger = get_script_logger(__file__)  # Get logger

    logger.info('Beginning...Simple Data Use Example...')

    logger.info('\tLoading gen-%s data...' % gen)

    # Load the S11 frequency-domain data
    s11_fd_data = load_pickle(os.path.join(__DATA_DIR,
                                           'fd_data_gen_%s_s11.pickle' % gen))

    logger.info('\t\tData loaded.')
    logger.info('\tLoading gen-%s metadata...' % gen)

    # Load the metadata of every scan
    metadata = load_pickle(os.path.join(__DATA_DIR,
                                        'metadata_gen_%s.pickle' % gen))

    # Create list of the unique ID number of each scan
    unique_ids = [md['id'] for md in metadata]

    logger.info('\t\tMetadata loaded.')

    logger.info('\tPlotting sample sinograms...')

    # For 10 random indices
    for rand_idx in np.random.randint(low=0,
                                      high=np.size(s11_fd_data, axis=0),
                                      size=[10, ]):

        # Get the metadata of this index
        tar_md = metadata[rand_idx]

        logger.info('\t\tPlotting sample ID %d...' % tar_md['id'])

        # If the scan corresponding to this index was not an
        # empty-chamber scan
        if not np.isnan(tar_md['emp_ref_id']):

            # Find the index of the experiment with the ID that
            # corresponds to the empty reference scan for this
            # target scan
            emp_idx = unique_ids.index(tar_md['emp_ref_id'])

            # Get the frequency-domain S11 measurements for the
            # target scan and the empty-chamber reference
            tar_data = s11_fd_data[rand_idx, :, :]
            emp_data = s11_fd_data[emp_idx, :, :]

            # Calibrate the target measurements by subtracting the
            # empty-chamber scan data
            cal_data = tar_data - emp_data

            # Convert to the time-domain via the ICZT
            cal_data = iczt(cal_data, ini_t=0, fin_t=6e-9, n_time_pts=1024,
                            ini_f=1e9, fin_f=8e9)

            # Plot the time-domain sinogram, displaying the measurements
            # of this scan after empty-chamber calibration
            plot_td_sinogram(cal_data, title='ID %d Sinogram' % tar_md['id'],
                             save_fig=True, dpi=300,
                             save_str=os.path.join(__OUTPUT_DIR, '%d_sino.png'
                                                   % tar_md['id']))

            logger.info('\t\t\tSample ID %d sinogram displayed.'
                        % tar_md['id'])

        else:  # If the rand_idx corresponds to an empty-chamber scan
            logger.info('\t\tERROR: Sample ID %d is an empty-chamber reference'
                        % tar_md['id'] + 'scan. No sinogram to plot.')

        logger.info('\t\tPrinting target experiment metadata to logger...')

        # Print each piece of metadata to the logger
        for md_info in tar_md.keys():
            logger.info('\t\t\t\t%s:\t%s' % (md_info, tar_md[md_info]))
