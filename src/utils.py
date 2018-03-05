# Copyright 2017 SuperDARN Canada
#
# Marina Schmidt
#
# exception.py
# 2018-01-26

from subprocess import call
import os
from convectionMapExceptions import RSTException, RSTFileEmptyException

def file_exists(filename):
    if not os.path.isfile(filename):
        raise IOError
    return True

def check_rst_command(rst_command, filepath):
    """
    Returns True if file is nt empty
    """
    return_value = call(rst_command, shell=True)
    if return_value != 0:
        raise RSTException(rst_command.split()[0], return_value)

    if os.path.getsize(filepath) > 0:
        return True
    else:
        raise RSTFileEmptyException(filename)
