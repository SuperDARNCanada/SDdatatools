# Copyright 2017 SuperDARN Canada
#
# Marina Schmidt
#
# exception.py
# 2018-01-26

from subprocess import check_output
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

def is_file_not_empty(filename):
    """
    Returns True if file is nt empty
    """
    if os.path.getsize(filename) >
        return True
    else
        raise RSTFileEmptyException(filename)

