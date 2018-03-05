# Copyright 2017 SuperDARN Canada
#
# Marina Schmidt
#
# exception.py
# 2018-01-26


class RSTException(Exception):

    def __init__(self, function_name, return_value):
        self.function_name = function_name
        self.return_value = return_value
        self.message = "RST function {function} failed with"\
                " error value of {returnvalue} "\
                "".format(function=function_name,
                          returnvalue=return_value)
        Exception.__init__(self, self.message)


class RSTFileEmptyException(Exception):

    def __init__(self, filename):
        self.filename = filename
        self.message = "RST file {} is empty".format(self.filename)
        Exception.__init__(self, self.message)

class NoGridFilesException(Exception):

    def __init__(self):
        self.message = "No grid files were produced"
        Exception.__init__(self, self.message)
