"""
Configuration
"""

# External packages
import configparser as cfg

# Path to configuration
PATH_CONFIG = "jobcore.conf"

# Functions
def get_configuration(section=None):
    config = cfg.ConfigParser()

    # Read configuration file
    config.read(PATH_CONFIG)

    # Return configuration
    return config if not section else config[section]
