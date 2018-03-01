# Copyright 2017 SuperDARN Canada
#
# Marina Schmidt
#
# exception.py
# 2018-01-26

from subprocess import call
import os
from convectionMapExceptions import RSTException, RSTFileEmptyException


def log_information(filename, verbose):
    """
    Logs information
    """
    pass


def check_rst_command(rst_command, filename):
    """
    Returns True if file is nt empty
    """
    return_value = call(rst_command.split())
    if return_value != 0:
        raise RSTException(rst_command, return_value)

    if os.path.getsize(filename) > 0:
        return True
    else:
        raise RSTFileEmptyException(filename)
