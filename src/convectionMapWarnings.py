# Copyright 2017 SuperDARN Canada
#
# Marina Schmidt
#
# warning.py
# 2018-01-26

import warnings


class OmniFileNotGeneratedWarning(Warning):

    def __init__(self, omni_filename, date):
        self.date = date
        self.omni_filename = omni_filename
        self.message = "Omni file: {filename}, was not generated for the "
        " date {date}. The omni data will not be used in the convection map "
        " process".format(filename=self.omni_filename,
                          date=self.date)
        Warning.__ini__(self, self.message)

class OmniFileNotFoundWarning(Warning):

    def __init__(self,omni_filename):
        self.omni_filename = omni_filename
        self.message = "{} file found was"
        " not found. The omni data will not be used in"
        " in the convection map process.".format(self.omni_filename)
        Warning.__init__(self, self.message)


class OmniBadDataWarning(Warning):

    def __init__(self,data):
        self.date = date
        self.message = "The IMF file for the date {} "
        " was not generated because there was no good data "
        " in the omni file".format(self.date)
        Warning.__init__(self, self.message)



