#!/usr/bin/env python

# Copyright 2017 SuperDARN Canada
#
# Marina Schmidt
#
# omni.py
# 2018-01-26

import os
import logging
from datetime import datetime, timedelta
from subprocess import check_output, call, CalledProcessError

from DARNprocessing.utils.convectionMapWarnings import (OmniBadDataWarning,
                                                        OmniFileNotFoundWarning,
                                                        OmniFileNotGeneratedWarning)
from DARNprocessing.utils.convectionMapExceptions import OmniException


class Omni():
    """
    The Omni class is used to check for omni file updates, get omni files from
    https://omniweb.sci.gsfc.nasa.gov/
    """

    def __init__(self, date, omni_path):

        if not logging:
            logfile = date + "_omni.log"
            logging.basicConfig(logfile, level=logging.DEBUG)
        else:
            logging.info("*** OMNI DATA ***")

        self.date = date
        self.omni_filename = "{}_omni.txt".format(self.date)
        self.imf_filename = "{}_imf.txt".format(self.date)
        self.omni_path = "{path}/{filename}".format(path=omni_path,
                                                    filename=self.omni_filename)
        self.imf_path = "{path}/{filename}".format(path=omni_path,
                                                   filename=self.imf_filename)
        logging.info("Searching for files:")
        logging.info(self.omni_filename)
        logging.info(self.imf_filename)

        self.start_time = str(date) + " 00:00"
        omni_start_datetime = datetime.strptime(self.start_time, "%Y%m%d %H:%M") -\
            timedelta(minutes=10)  # Omni time delay is ~10 minutes
        self.omni_start_time = omni_start_datetime.strftime("%Y%m%d%H")

    def get_data_availability(self):
        """
        get data availability, get the most updated data availability off of:
            https://omniweb.gsfc.nasa.gov/html/ow_data.html for IMF data.
            :retun datetime: retruns a datetime object that is the current
                             data avialability date.
        """
        omni_date = datetime.strptime(self.start_time, "%Y%m%d %H:%M")
        omni_year = omni_date.strftime("%Y")

        # scrapes the omni website for the IMF data availability date by looking
        # by looking for the most recent year 1963 in their database and IMF
        # label.
        curl_command = "curl https://omniweb.gsfc.nasa.gov/html/ow_data.html 2>/dev/null | grep '1963.*IMF' "
        logging.info('Getting OMNI data availability:')
        logging.info(curl_command)

        try:
            omni_update_time = check_output(curl_command, shell=True)
        except CalledProcessError as e:
            logging.warn("Could not get the date the"
                         " last time the file was updated.")
            raise OmniException(e)

        # returns the omni updated time as a datetime object
        return datetime.strptime(omni_update_time.split(" ")[3],"%Y-%m-%d")

    def check_for_updates(self, omni_filename=None):
        """
        Cross checks if the omni file on the website has been updated
        since the last time it was downloaded. This ensures most recently
        updated data for the convection map process.

        Returns true if the omni file on the website has been updated since
        the last download.
        """
        logging.info("Checking for updates for OMNI file:")
        if omni_filename:
            self.omni_filename = omni_filename

        omni_file_path = "{omnipath}/{omnifile}"\
                         "".format(omnipath=self.omni_path,
                                   omnifile=self.omni_filename)

        if not os.path.isfile(omni_file_path):
            raise OmniFileNotFoundWarning()

        try:
            omni_modified_date = self.get_data_availability()
        except OmniException as e:
            logging.warning("Exception from get_update_omni_date {}".format(e))
            return False

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
        logging.info("Downloading new OMNI file:")
        curl_command = 'curl -d  '\
                       '"activity=ftp&res=min&spacecraft=omni_min&'\
                       'start_date={start_time}&end_date={date}23&vars=13&'\
                       'vars=14&vars=17&vars=18&submit=Submit" '\
                       'https://omniweb.sci.gsfc.nasa.gov/cgi/nx1.cgi'\
                       ' | grep -oh http.*.lst\\"'\
                       ' | grep -oh http.*.lst'.format(start_time=self.omni_start_time,
                                                       date=self.date)

        logging.info(curl_command)
        # I am aware that using shell=True on a subprocess method is
        # a security risk, however, to get the curl command to work
        # I have to use shell=True
        # as there is some parsing problem that happens when it is False :/
        # I have also tried to install pycurl but that was head in a half so
        # I am sticking with this :)
        try:
            omnifile_url = check_output(curl_command, shell=True)
        except CalledProcessError as e:
            raise OmniException(e)

        if "https" not in str(omnifile_url):
            omnifile_url = str(omnifile_url).replace('http', 'https')
        omnifile_url = omnifile_url.strip("b'")
        omnifile_url = omnifile_url.strip("\\n'")
        download_file_command = "curl -o {omni_file}"\
                " {link}".format(link=omnifile_url,
                                 omni_file=self.omni_path)
        logging.info(download_file_command)

        try:
            call(download_file_command.split())
        except CalledProcessError as e:
            logging.warning('An error occurred and OMNI file was not',
                            'downloaded. A magnetic field of [0,0,0] will',
                            'be used instead.')
            raise OmniFileNotGeneratedWarning(self.omni_filename,
                                              self.date)

        if (not os.path.isfile(self.omni_path) and
           os.path.getsize(self.omni_path) < 0):
            raise OmniFileNotGeneratedWarning(self.omni_filename,
                                              self.date)

    def omnifile_to_IMFfile(self, omni_filename=None):
        """
        Parses the omni file into a IMF file format such that the RST code can
        use it the convection map process.
        """
        logging.info("Converting OMNI file to IMF format for RST")
        if omni_filename:
            self.omni_filename = omni_filename

        try:
            with open(self.omni_path, 'r') as omni_file:
                omni_data_list = omni_file.read().splitlines()
        except (IOError, NameError):
            raise OmniFileNotFoundWarning(self.omni_filename)

        # TODO: implement a scheme to parse out solar wind when included in the omni data
        imf_file = open(self.imf_path, 'w')
        bad_data_counter = 0

        #  Generate the IMF file from the omni data
        for omni_data in omni_data_list:

            # doy: day of year
            (omni_year, omni_doy, omni_hour, omni_minute, omni_BM,
             omni_Bx, omni_By, omni_Bz) = omni_data.split()

            #  first day of the year + number of days - 1 <-- minus 1 because
            #  we need to acount for the first day already added in with doy.
            omni_date = datetime(int(omni_year), 1, 1)\
                + timedelta(int(omni_doy) - 1)

            omni_month = omni_date.strftime("%m")
            omni_day = omni_date.strftime("%d")

            imf_line = "{year} {month} {day} {hour} {minute} 00 "\
                       "{Bx} {By} {Bz}\n".format(year=omni_year,
                                                 month=omni_month,
                                                 day=omni_day,
                                                 minute=omni_minute,
                                                 hour=omni_hour, Bx=omni_Bx,
                                                 By=omni_By, Bz=omni_Bz)
            imf_file.write(imf_line)
            if float(omni_BM) > 999.0:
                bad_data_counter = bad_data_counter + 1
        imf_file.close()
        if bad_data_counter == len(omni_data_list):
            os.remove(self.imf_path)
            raise OmniBadDataWarning(self.date)


if __name__ == '__main__':
    omni = Omni("20180810", "./")
    omni.get_omni_file()
