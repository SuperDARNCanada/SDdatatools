# Copyright 2017 SuperDARN Canada
#
# Marina Schmidt
#
# exception.py
# 2018-01-26
"""
Class of exceptions that are specific to the convection map process
"""


class OmniException(Exception):
    """
    Exception for when there is an error in getting the Omni file from:
            https://omniweb.gsfc.nasa.gov/
    Parameter:
    :param message: error message obtained when getting the omni file from curl
    """
    def __init__(self, message):
        self.message = message
        Exception.__init__(self, self.message)


# TODO: Move these exception to a FileExceptions file, RSTEceptions, ... etc
class PathDoesNotExistException(Exception):
    """
    Exception for when a path does not exist, typically used on the datapath.
    Parameter:
    :param path: the path that does not exist
    """
    def __init__(self, path):
        self.path = path
        self.message = "Path: {} does not exist".format(path)
        Exception.__init__(self, self.message)

class FileDoesNotExistException(Exception):
    """
    Exception when a file does not exist.

        :param filename: absolute path including the filename
    """

    def __init__(self, filename):
        self.filename = filename
        self.message = "Error: {} does not exist, please makes sure the spelling and path is correct."
        Exception.__init__(self,self.message)

class UnsupportedTypeException(Exception):
    """
    Exception when a file/compression type is not supported or is not implemented
    in the process.
        :param message: message of what is not supported and what is.
    """

    def __init__(self, message):
        self.message = message
        Exception.__init__(self, self.message)


class RSTException(Exception):
    """
    Exception for when a RST function fails
    Parameters:
        :param function_name: name of the RST function
        :param return_value: the return value the RST function returned
    """
    def __init__(self, function_name, return_value):
        self.function_name = function_name
        self.return_value = return_value
        self.message = "RST function {function} failed with"\
            " error value of {returnvalue} "\
            "".format(function=function_name,
                      returnvalue=return_value)
        Exception.__init__(self, self.message)


class RSTFileEmptyException(Exception):
    """
    Exception when a RST function returns an empty file
    parameters:
        :param filename: name of the file that was empty
    """
    def __init__(self, filename):
        self.filename = filename
        self.message = "RST file {} is empty".format(self.filename)
        Exception.__init__(self, self.message)

class NoGridFilesException(Exception):
    """
    Exception when no grid files were produced
    parameters:
        :param radar_list: list of radar acronyms that were used for trying to
                           produce grid files
    """
    def __init__(self, radar_list):
        self.message = "No grid files were produced for the following radars: "
        for radar in radar_list:
            self.message += " {},".format(radar)
        Exception.__init__(self, self.message)
