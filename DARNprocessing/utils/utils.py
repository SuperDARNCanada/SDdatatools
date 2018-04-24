# Copyright 2017 SuperDARN Canada
#
# Marina Schmidt
#
# exception.py
# 2018-01-26

import os
import logging
from subprocess import call
from glob import glob

from DARNprocessing.utils.convectionMapExceptions import (RSTException,
                                                          RSTFileEmptyException)

def file_exists(filename):
    """
    Checks if a file exists if not raises an IOError
    """
    if not os.path.isfile(filename):
        message = "{} does not exists".format(filename)
        raise IOError(message)
    return True

def check_rst_command(rst_command, filepath):
    """
    Runs RST command and checks if they returned succeful and
    the file was properly produced.

    Returns True if file is not empty
    """
    if logging:
        logging.info(rst_command)

    return_value = call(rst_command, shell=True)
    if return_value != 0:
        raise RSTException(rst_command.split()[0], return_value)

    for filename in glob(filepath):
        if os.path.getsize(filename) > 0:
            return True
        else:
            raise RSTFileEmptyException(filename)
