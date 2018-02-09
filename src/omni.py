#!/usr/bin/env python

# Copyright 2017 SuperDARN Canada
#
# Marina Schmidt
#
# omni.py
# 2018-01-26

from datetime import datetime, timedelta
from subprocess import check_output, call
from convectionMapWarnings import *
from constants import *
import warnings
import os
import shutil


class Omni():
    """
    """

    def __init__(self, date, omni_path):

        self.date = date + " 00:00"
        self.omni_path = omni_path
        self.omni_filename = "omni_{}.txt".format(self.date)
        self.imf_filename = "imf_{}.txt".format(self.date)


        omni_start_datetime = datetime.strptime(self.date, "%Y%m%d %H%m") -\
            timedelta(minutes=10)  # Omni time delay is ~10 minutes
        self.omni_start_time = omni_start_datetime.strftime("%Y%m%d%H")

    def check_for_updates(self,omni_filename=None):
        """
        Cross checks if the omni file on the website has been updated
        since the last time it was downloaded. This ensures most recently
        updated data for the convection map process.

        Returns true if the omni file on the website has been updated since
        the last download.
        """
        if omni_filename:
            self.omni_filename = omni_filename

        omni_file_path = "{}/{}".format(self.omni_path,self.omni_filename)

        if not os.path.isfile(omni_file_path):
            raise OmniFileNotFoundWarning(omni_filename)

        omni_date = datetime.strptime(self.date, "%Y%m%d0 %H%m")
        omni_year = omni_date.strftime("Y")

        curl_command = "curl -sI "
                       "ftp://spdf.gsfc.nasa.gov/pub/data/omni/high_res_omni/omni_min{}.asc "
                       "| grep Last-Modified "
                       "| sed 's/Last-Modified: //'".format(omni_year)


        try:
            omni_update_time = check_output(curl_command,shell=True)
        except CalledProcessError:
            print("Warning: could not get the date the"
                  " last time the file was updated")
            return False

        #  "%a, %d %b %Y %H:%M:%S %Z\r\n" is the format the the date is parsed
        # from the website. example: 'Mon, 29 Jan 2018 14:56:10 GMT\r\n'
        omni_modified_date = datetime.strptime(omni_update_time,
                                               "%a, %d %b %Y %H:%M:%S %Z\r\n")

        local_omni_modified_date = datetime.fromtimestamp(
                                 os.path.getmtime(omni_file_path))

        modification_diff = local_omni_modified_date - omni_modified_date
        if modification_diff.total_seconds() > 0:
            return False
        else:
            return True

    def get_omni_file(self):
        """
        Downloads the omni file for the given date.

        """


        curl_command = 'curl -d  '\
                      '"activity=ftp&res=min&spacecraft=omni_min&'\
                      'start_date={start_time}&end_date={date}23&vars=13&'\
                      'vars=14&vars=17&vars=18&submit=Submit" '\
                      'https://omniweb.sci.gsfc.nasa.gov/cgi/nx1.cgi'\
                      ' | grep -oh http.*.lst\\"'\
                      ' | grep -oh http.*.lst'.format(
                             start_date=self.omni_start_time,
                             date=self.date)

        # I am aware that using shell=True on a subprocess method is
        # a security risk, however, to get the curl command to work
        # I have to use shell=True
        # as there is some parsing problem that happens when it is False :/
        # I have also tried to install pycurl but that was head in a half so
        # I am sticking with this :)
        try:
            omnifile_url = check_output(curl_command, shell=True)
        except CalledProcessError:
            warnings.warn('', OmniFileWarning(self.date))
            return ErrorCodes.ERROMNIFILE


        if "https" not in omnifile_url:
            omnifile_url = omnifile_url.replace('http','https')

        download_file_command = 'curl {link} > {filename}'.format(link=omni_url,\
                                                                  filename=\
                                                                  self.omni_filename)

        return_value = call(download_file_command,shell=True)
        if return_value != 0:
            warning.warn('',OmniFileNotGeneratedWarning(self.omni_filename,
                                                        self.date))
            return ErrorCodes.ERROMNIFILE

        if ! os.path.isfile(self.omni_filename) and\
           os.path.getsize(self.omni_filename) < 0:
            warning.warn('',OmniFileNotGeneratedWarning(self.omni_filename,
                                                        self.date))
            return ErrorCodes.ERROMNIFILE

        try:
            shutil.copy2(self.omni_filename, self.omni_path)
        except shutil.Error as err:
            warning.warn('Warning: {}'.format(err),UserWarning)
        return 0  # 0 means success in this situation

    def omnifile_to_IMFfile(self,omni_filename=None):
        """
        Parses the omni file into a IMF file format such that the RST code can
        use it the convection map process.
        """
        if omni_filename:
            self.omni_filename=omni_filename

        try:
            with open(self.omni_filename, 'r') as omni_file:
                omni_data_list = omni_file.read().splitlines()
        except IOError, NameError:
            warning.warn('',OmniFileNotFoundWarning(self.omni_filename))
            return ErrorCodes.ERROMNIFILE

#
# TODO: implement a scheme to parse out solar wind when included in the omni data
#
        imf_file = open(self.imf_filename,'w')
        bad_data_counter = 0

        #  Generate the IMF file from the omni data
        for omni_data in omni_data_list:

            #doy: day of year
            omni_year, omni_doy, omni_hour, omni_minute, omni_BM,
            omni_Bx, omni_By, omni_Bz = omni_data.split()

            #  first day of the year + number of days - 1 <-- minus 1 because
            #  we need to acount for the first day already added in with doy.
            omni_date = datetime(int(omni_year), 1, 1) +
                        timedelta(int(omni_doy) - 1)

            omni_month = omni_date.strftime("%m")
            omni_day = omni_date.strftime("%d")

            imf_line = "{year} {month} {day} {hour} {minute} 00 "
            "{Bx} {By} {Bz}\n".format(year = omni_year, month = omni_month,
                                    day = omni_day, minute = omni_minute,
                                    hour = omni_hour, Bx = omni_Bx,
                                    By = omni_By, Bz = omni_Bz)
            imf_file.write(imf_line)

            if float(omni_BM) > 999.0:
                bad_data_counter = bad_data_counter + 1

        imf_file.close()
        if bad_data_counter == len(omni_data_list):
            os.remove(self.imf_filename0)
            warning.warn('',OmniBadDataWarning(self.date))
            return ErrorCodes.ERROMNIBADDATA

        try:
            shutil.copy2(self.imf_filename, self.omni_path)
        except shutil.Error as err:
            warning.warn('Warning: {}'.format(err),UserWarning)

        return 0  # 0 means success in this situation















