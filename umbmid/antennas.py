"""
Tyson Reimer
University of Manitoba
October 19th, 2019
"""

###############################################################################


def get_phase_delay_rad(scan_rad):
    """Returns the modified antenna rad, accounting for phase delay

    The antennas used in our pre-clinical system introduce a phase
    delay, which can be modeled as an increase in the antenna
    trajectory radius. The phase delay was determined experimentally
    in [1].

    1. D. Rodriguez-Herrera, "Antenna characterisation and optimal
       sampling constraints for breast microwave imaging systems with
       a novel wave speed propagation algorithm," M.Sc. Thesis,
       University of Manitoba, 2016.

    Parameters
    ----------
    scan_rad : float
        The radius of the antenna trajectory in the scan, as measured
        from the SMA connection point on the antennas

    Returns
    -------
    delayed_rad : float
        The radius of the antenna trajectory in the scan, accounting
        for the phase delay introduced by the antenna
    """

    # Use empircal formula from the thesis by D. Rodriguez-Herrera
    delayed_rad = 0.97 * (scan_rad - 0.106) + 0.148

    return delayed_rad
