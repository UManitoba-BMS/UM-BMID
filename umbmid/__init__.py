"""
Tyson Reimer
University of Manitoba
July 26th, 2019
"""

import os
import sys
import logging
import logging.handlers
from socket import gethostname
from pathlib import Path

###############################################################################


class NullLogger:

    def critical(self, *args):
        pass

    def error(self, *args):
        pass

    def warning(self, *args):
        pass

    def info(self, *args):
        pass

    def debug(self, *args):
        pass


null_logger = NullLogger()

###############################################################################


def get_proj_path():
    """Returns the path to the project-level directory.

    Returns
    -------
    proj_path : str
        The str for the project path
    """
    proj_path = Path(__file__).parents[1]

    return proj_path


def verify_path(path):
    """If path exists, do nothing, else make it exist.

    Parameters
    ----------
    path : str
        The path to investigate - NOTE: will only 'make it exist' if
        only the most-nested dir does not exist, but all parent
        directories do exist.
    """

    if not os.path.isdir(path):  # If the path does not exist
        os.mkdir(path)  # Make it exist

    else:  # If the path exists
        pass  # Do nothing


def get_script_logger(script_path, level=logging.DEBUG):
    """

    Parameters
    ----------
    script_path : str
        Path to the script that will use the logger
    level :
        Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)

    Returns
    -------
    logger :
        Logger
    """

    # Define the format for logging
    log_format = '[%(asctime)-8s][%(levelname)s][%(filename)s:%(lineno)s]:' \
                 '\t%(message)s'

    # #############   #####
    # Logging Level - Value
    # CRITICAL        50
    # ERROR           40
    # WARNING         30
    # INFO            20
    # DEBUG           10
    # NOTSET          0

    # Verify that the log dir exists
    verify_path(os.path.join(get_proj_path(), 'output/logs/'))

    # Find the name of the script that will be used
    script_name = os.path.splitext(os.path.basename(script_path))[0]

    # Get the name of the .log file that will be written to
    log_fname = "%s/output/logs/%s_%s.log" % (get_proj_path(), gethostname(),
                                              script_name)

    # Define the file handler
    file_handler = logging.handlers.RotatingFileHandler(log_fname,
                                                        maxBytes=1024 * 1024,
                                                        backupCount=100)
    file_handler.setFormatter(logging.Formatter(log_format))

    # Define the stdout handler
    stdout_handler = logging.StreamHandler(sys.stdout)
    stdout_handler.setFormatter(logging.Formatter(log_format))

    # Get the logger
    logger = logging.getLogger(script_name)

    # required if you don't want to exit the shell between 2 executions
    del (logger.handlers[:])

    logger.setLevel(level)
    logger.addHandler(file_handler)
    logger.addHandler(stdout_handler)

    logger.info("UM-BMID Logger initialized in host [%s]." % (gethostname()))

    return logger
