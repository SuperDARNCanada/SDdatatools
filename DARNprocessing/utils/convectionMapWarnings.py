# Copyright 2017 SuperDARN Canada
#
# Marina Schmidt
#
# warning.py
# 2018-01-26
"""
Warnings for the convection map process
"""


class OmniFileNotGeneratedWarning(Warning):
    """
    Warning when the Omni file was not downloaded from the webpage:
            https://omniweb.gsfc.nasa.gov/
        Parameters:
            :param omni_filename: file name of the omni file
            :param date: date trying to obtain for the omni file
    """
    def __init__(self, omni_filename, date):
        self.date = date
        self.omni_filename = omni_filename
        self.message = "Omni file: {filename}, was not generated for the "\
            "date {date}. The omni data will not be used in the "\
            "convection map  process".format(filename=self.omni_filename,
                                             date=self.date)
        Warning.__init__(self, self.message)


class OmniFileNotFoundWarning(Warning):
    """
    Warning when an omni file is not found for comparing if the file should be
    updated.
        Parameters:
            :param omni_filename: file name of the omni file
    """
    def __init__(self):
        self.message = "No ONMI file was found "
        Warning.__init__(self, self.message)


class OmniBadDataWarning(Warning):
    """
    Warning when the omni file download has no good data - example when the file
        contains only values of 9999
        Parameters:
            :param date: the date of omni data
    """
    def __init__(self, date):
        self.date = date
        self.message = "The IMF file for the date {} "\
            " was not generated because there was no good data "\
            " in the omni file".format(self.date)
        Warning.__init__(self, self.message)


class EmptyDataFileWarning(Warning):
    """
    Warning when the data file is empty but does not effect the process
        Parameters:
            :param data_file: data file name that is empty
            :param process: the name of the process that the file is used in
    """
    def __init__(self, data_file, process):
        self.data_filename = data_file
        self.message = "Data file {filename} is Empty, will not be used in the"\
            " {processname} process".format(filename=self.data_filename,
                                            processneame=process)
        Warning.__init__(self, self.message)


class FileNotFoundWarning(Warning):
    """
    Warning when a file is not found but does not effect the process
        Parameters:
            :param data_file: file name of the data file
            :param process: process name
    """
    def __init__(self, data_file, process):
        self.data_filename = data_file
        self.message = "Data file {filename} does not exist,"\
            " will not be used in the"\
            "{processname} process".format(filename=self.data_filename,
                                           processname=process)
        Warning.__init__(self, self.message)


class ConvertWarning(Warning):
    """
    Warning convert command to change the plot type from ps to the image
        extension passed by user.
        Parameters:
            :param ps_file: ps file name generated
            :param extension: extension type the user passed in
    """
    def __init__(self, ps_file, extension):
        self.ps_file = ps_file
        self.extension = extension

        self.message = "Warning: convert command could not convert "\
            "{ps_filename} to {ext} format".format(ps_filename=ps_file,
                                                   ext=extension)
        Warning.__init__(self, self.message)
