"""
Loading
"""

# External packages
import pickle as pkl

# Data path
PREFIX_PATH = 'data/'

# Functions
def load_variable(filename) -> object:
    f = open(PREFIX_PATH + filename, 'rb')

    variable = pkl.load(f)

    f.close()

    return variable
