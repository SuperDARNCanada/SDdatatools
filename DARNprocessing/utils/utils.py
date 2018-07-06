# Copyright 2017 SuperDARN Canada
#
# Marina Schmidt
#
# exception.py
# 2018-01-26

import os
import logging
import argparse
from subprocess import call
from glob import glob

from DARNprocessing.utils.convectionMapExceptions import (RSTException,
                                                          RSTFileEmptyException)


def flag_options(program_name,program_desc,option_names,option_settings):
    """
    Parameter options is a utility to add options to runnable scripts

        :param program_name: name of the program
        :param program_desc: description of the program
        :param options: dictionary of dictionaries containing
                        the following structure:
                        { '<option name>': {''}
                            *Note: for required options do not use a hyphen,
                                   for flag options use a single hyphen for
                                   singlular letters and two hyphens for words
        :return options_object: passes back an options object the method can
                                invoke to obtain the values from sys.argv

    """
    parser = argparse.ArgumentParser(prog=program_name,
                                     description=program_desc)
    # required arguement
    for option_name, option_setting in zip(option_names,option_settings):
        if len(option_name) == 1:
            parser.add_argument(*option_name,**option_setting)
        else:
            parser.add_argument(*option_name,**option_setting)


    parameter = parser.parse_args()
    return vars(parameter)

def file_exists(filename):
    """
    Checks if a file exists if not raises an IOError

        :param filename: name of the file name to check
        :return: boolean true if file exists
        :raises IOError: if file does not exist
    """
    if not os.path.isfile(filename):
        message = "{} does not exists".format(filename)
        raise IOError(message)
    return True


def check_rst_command(rst_command, filepath):
    """
    Runs RST command and checks if they returned succeful and
    the file was properly produced.

        :param rst_command: the string of the rst command to be
                            called in a terminal
        :param filename: the file name that is produced by the command
        :raise RSTExceptopm: raises an error when rst returns a
                             non-zero return value
        :raise RSTFileEmptyException: raise an error when the output
                                      file is empty
    """
    if logging:
        logging.info(rst_command)

    return_value = call(rst_command, shell=True)
    if return_value != 0:
        # first word of the rst_command should be the rst command name
        raise RSTException(rst_command.split()[0], return_value)

    for filename in glob(filepath):
        if os.path.getsize(filename) <= 0:
            raise RSTFileEmptyException(filename)
