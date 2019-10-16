"""
Tyson Reimer
University of Manitoba
October 15th, 2019
"""

import pkg_resources  # Package is included in Python

with open('..\\requirements.txt', 'rb') as file:

    # Get the required package names
    package_names = [ff.strip().decode('utf-8') for ff in file]

    # Check to see if they're installed
    pkg_resources.require(package_names)
