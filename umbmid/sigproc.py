"""
Tyson Reimer
University of Manitoba
July 26th, 2019
"""

import numpy as np

###############################################################################


def iczt(fd_data, ini_t, fin_t, n_time_pts, ini_f, fin_f):
    """Compute the ICZT of the fd_data, transforming to the time-domain.

    NOTE: Currently supports 1D or 2D fd_data arrays, and will perform
    the transform along the 0th axis of a 2D array

    Parameters
    ----------
    fd_data : array_like
        The frequency-domain array to be transformed via the ICZT to the
        time-domain
    ini_t : float
        The starting time-of-response to be used for computing the ICZT,
        in seconds
    fin_t : float
        The stopping time-of-response to be used for computing the ICZT,
        in seconds
    n_time_pts : int
        The number of points in the time-domain at which the transform 
        will be evaluated
    ini_f : float
        The initial frequency used in the scan, in Hz
    fin_f : float
        The final frequency used in the scan, in Hz

    Returns
    -------
    td_data : array_like
        Array of the transformed data
    """

    n_freqs = fd_data.shape[0]  # Find the number of frequencies use

    # Find the conversion factor to convert from time-of-response to
    # angle around the unit circle
    time_to_angle = (2 * np.pi) / np.max(get_scan_times(ini_f, fin_f, n_freqs))

    # Find the parameters for computing the ICZT over the specified
    # time window
    theta_naught = ini_t * time_to_angle
    phi_naught = (fin_t - ini_t) * time_to_angle / (n_time_pts - 1)

    # Compute the exponential values only once
    exp_theta_naught = np.exp(-1j * theta_naught)
    exp_phi_naught = np.exp(-1j * phi_naught)

    # Make a dummy vector to facilitate vectorized computation
    dummy_vec = -1 * np.arange(n_freqs)

    # Make dummy vector of time points to facilitate vectorized
    # computation
    time_pts = np.arange(n_time_pts)

    # Find the z-value matrix, to facilitate vectorized computation
    z_vals = exp_theta_naught * exp_phi_naught**time_pts
    zs_power = np.power(z_vals[None, :], dummy_vec[:, None])

    # If computing over a 2D array
    if len(fd_data.shape) > 1:

        # Init array to return
        td_data = np.zeros([n_time_pts, fd_data.shape[1]], dtype=complex)

        # For each antenna position
        for ant_pos in range(np.size(fd_data, axis=1)):

            # Find the ICZT
            td_data[:, ant_pos] = np.sum(fd_data[:, ant_pos][:, None] *
                                         zs_power, axis=0) / n_freqs

    else:  # If the fd_data is a 1D array

        # Find the ICZT
        td_data = np.sum(fd_data[:, None] * zs_power, axis=0) / n_freqs

    # Apply phase compensation
    td_data = phase_compensate(td_data, ini_f=ini_f, ini_t=ini_t, fin_t=fin_t,
                               n_time_pts=n_time_pts)

    return td_data


def get_scan_freq_step(ini_f, fin_f, n_freqs):
    """Gets the incremental frequency step used in the scan.

    Parameters
    ----------
    ini_f : float
        The initial frequency used in the scan, in Hz
    fin_f : float
        The final frequency used in the scan, in Hz
    n_freqs : int
        The number of frequencies used in the scan

    Returns
    -------
    freq_step : float
        The incremental frequency step, in Hz
    """

    # The scan-frequency vector
    freqs = np.linspace(ini_f, fin_f, n_freqs)

    # Get the incremental freq step size
    freq_step = freqs[1] - freqs[0]

    return freq_step


def get_scan_times(ini_f, fin_f, n_freqs):
    """Returns the vector of time-points as obtained via the IDFT

    Parameters
    ----------
    ini_f : float
        The initial frequency used in the scan, in Hz
    fin_f : float
        The final frequency used in the scan, in Hz
    n_freqs : int
        The number of frequencies used in the scan

    Returns
    -------
    scan_times : array_like
        The vector of time-points used to represent the time-domain
        signal, as obtained by the IDFT
    """

    # Get the incremental freq step
    freq_step = get_scan_freq_step(ini_f, fin_f, n_freqs)

    # Get the incremental time-step
    time_step = 1 / (n_freqs * freq_step)

    # Define the vector of the time-points
    scan_times = np.linspace(0, n_freqs * time_step, n_freqs)

    return scan_times


def phase_compensate(td_data, ini_f, ini_t, fin_t, n_time_pts):
    """Applies phase compensation to TD signals obtained with the ICZT

    Parameters
    ----------
    td_data : array_like
        Time-domain signals obtained via the ICZT
    ini_f : float
        Initial frequency used in the scan, in Hz
    ini_t : float
        Initial time point of the td_data, in seconds
    fin_t : float
        Final time point of the td_data, in seconds
    n_time_pts : int
        Number of time-points used to create the td_data

    Returns
    -------
    compensated_td_data : array_like
        Time-domain signals after phase compensation
    """

    n_dim = len(np.shape(td_data))

    assert n_dim in [1, 2], "td_data must be 1D or 2D arr"

    # Create vector of the time points used to represent the td_data
    time_vec = np.linspace(ini_t, fin_t, n_time_pts)

    # Phase correction factor
    phase_fac = np.exp(1j * 2 * np.pi * ini_f * time_vec)

    if n_dim == 1:  # If td_data was 1D arr

        compensated_td_data = td_data * phase_fac  # Apply to measured data

    else:  # If td_data was 2D arr

        compensated_td_data = td_data * phase_fac[:, None]

    return compensated_td_data
