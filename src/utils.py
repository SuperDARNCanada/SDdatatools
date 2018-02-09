# Copyright 2017 SuperDARN Canada
#
# Marina Schmidt
#
# exception.py
# 2018-01-26

from subprocess import check_output, call
import os
from convectionMapExceptions import *

def get_datafiles(superdarn_data):
    """
    Copies the radar data files for the given date, hemisphere
    and format to the destination path.
    """
    pass


def log_information(filename,verbose):
    """
    Logs information
    """
    pass

def command_line_interface():
    pass

def check_for_channel(channel_number=0):
    pass

def check_rst_command(rst_command,filename):
    """
    Returns True if file is nt empty
    """
    return_value = call(rst_command.split())
    if return_value != 0:
        raise RSTException(rst_command,return_value)

    if os.path.getsize(filename) > 0:
        return True
    else
        raise RSTFileEmptyException(filename)

