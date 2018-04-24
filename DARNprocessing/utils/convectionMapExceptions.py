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
    Exeception for when trying to curl the omni file for dowloading.
    """
    def __init__(self, message):
        self.message = message
        Exception.__init__(self, self.message)

class PathDoesNotExistException(Exception):
    """
    Exception for when a path does not exist, typically used on the datapath.
    parameter:
        path : the path that does not exist
    """
    def __init__(self, path):
        self.path = path
        self.message = "Path: {} does not exist".format(path)
        Exception.__init__(self, self.message)


class RSTException(Exception):
    """
    Exception for when a RST function fail
    Parameters:
        function_name: name of the RST function
        return_value: the return value the RST function returned
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
        filename: name of the file that was empty
    """
    def __init__(self, filename):
        self.filename = filename
        self.message = "RST file {} is empty".format(self.filename)
        Exception.__init__(self, self.message)

class NoGridFilesException(Exception):
    """
    Exception when no grid files were produced
    parameters:
        None
    """
    def __init__(self):
        self.message = "No grid files were produced"
        Exception.__init__(self, self.message)
