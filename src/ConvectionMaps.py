#!/usr/bin/env python

# Copyright 2017 SuperDARN Canada
#
# Marina Schmidt
#
# fitacf2convectionMap.py
# 2018-01-26

from datetime import datetime
from distutils.dir_utili import mkpath
from multiprocess import Pool
from subprocess import call
from globl import glob

from convectionconstants import *

import shutil
import os
import sys
import argparse
import re

class ConvectionMaps():

    def __init__(self,arguements):
        """
        Reads in user command line options and parses them to correct member
        fields.
        """

        self._current_date = datetime.now()
        self._current_path = os.getcwd()

        #
        # TODO: place this in utils module if other scripts have similar options
        #

        parser = argparse.ArgumentParser(prog='fitacf2convectionmap',description='Converts fitacf files'
                                         ' to convection maps')
        # required arguement
        parser.add_argument('date',type=str,
                            help='The date of the fitacf data.'
                            ' Format: YYYYMMDD')

        # RST options
        parser.add_argument('-c','--channel',type=str,
                            choices=[0,1,2,3,4,5],default='5',
                            help='Select the channel number of data'
                            ' to use for the convection map process.'
                            ' Default: 5 - use all channels')

        parser.add_argument('--hemisphere',type=str,
                            choices=['north','south'],default='both',
                            help='The hemisphere you want to assimilate.'
                            ' Default: north')
        parser.add_argument('--start-time',type=str,
                            metavar='hh:mm',default='00:00',
                            help='The start time at hh:mm of the fitacf data.'
                            ' Default: 00:00')
        parser.add_argument('--end-time',type=str,
                            metavar='hh:mm',default='23:59',
                            help='The end time at hh:mm of the fitacf data.'
                            ' Default: 23:59')
        parser.add_argument('--rst-version',type=float,
                            metavar='N',default=4.1,
                            help='The version number of RST that'
                            ' you are using. Default: 4.1')
        parser.add_argument('-i','--image-extension',type=str,
                            metavar='EXTENSION',default='pdf',
                            help='The image format of convection maps.'
                            ' Default: pdf')

        # This was going to be used in the case of a general script, however,
        # I am currently not sure which steps are needed for various data
        # formats and in the future is might be easier for the user to
        # to inherit this class and then modify as needed for the format.
        # TODO: decide whether this should be taken out.
        # parser.add_argument('-f','--data-format',type=str,
        #                    choices=['fitacf','fit','fitred'],default='fitacf ',
        #                    help='The data format to use for generating the'
        #                    ' convection maps Default: fitacf')

        # Path options
        parser.add_argument('-d','--datapath', type=str,
                             metavar='PATH', default=self.current_path,
                             help='The absolute path to the fitacf data.'
                            ' Default: {}'.format(self.current_path))
        parser.add_argument('-p','--plotpath',type=str,
                            metavar='PATH', default=self.current_path,
                            help='The absolute path to where the convection'
                            ' maps will be saved.'
                            ' Default: {}'.format(self.current_path))
        parser.add_argument('-o','--omnipath', type=str,
                            metavar='PATH', default=self.current_path,
                            help='The absolute path to where the omni files'
                            ' will be saved to.'
                            ' Default: {}'.format(self.current_path))
        # Parallel options
        parser.add_argument('-n', type=int,
                            metavar='NUMPROCESSORS', default=1,
                            help='The number of processors you wish to use'
                            ' in parallel mode. '
                            ' This option enables parallel mode.'
                            ' Default: 1')

        # Standard options, note: the help option is handled by argparse
        parser.add_argument('-v','--verbose', action='store_true',
                            help='Turns on verbose mode.')


        self.parameter = parser.parse_args()
        self.channel = ['','a','b','c','d']

        if self.parameter['rst-version'] < 4.1:
            self.rst_options = "-new "



    def setup_paths(self):
        """
        setup the folder organization for archiving data
        """
        folder_oragnization = '{date}/{hemisphere}/{currentdate}'
                              ''.format(date = self.parameter['date'],
                                        hemisphere = self.parameter['hemisphere'],
                                        currentdate =
                                        self._current_date.strftime("%Y%m%d"))
        self.parameter['plotpath'] = self.parameter['plotpath'] + \
                                     folder_organization
        self.parameter['mappath'] = self.parameter['mappath'] + \
                                    folder_organization

        mkpath(self.parameter['plotpath'])
        mkpath(self.parameter['mappath'])

#TODO: implement parallel version

    def _generate_radar_grid_file(self,radar_ext):

        data_date = datetime.strptime(self.parameter['date'],"%Y%m%d")
        data_year = data_date.strftime("%Y")
        data_month = data_date.strftime("%m")

        search_pattern = './{date}*{ext}'.format(data =self.parameter['date'],
                                                 ext = radar_ext)
        grid_search_pattern = '{}.grid'.format(search_pattern)

        if not os.path.isfile(search_pattern):
            data_path = "{datapath}/{year}/{month}/"
                        "{datafile}.gz".format(datapath =
                                               self.parameter['date'],
                                               year = data_year,
                                               month = data_month,
                                               datafile = search_pattern)
            try:
                shutil.copy2(data_path,'.')
            except shutil.Error:
                return ErrorCodes.ERRFILENOTFOUND

            gzip_command = "gzip -d {}.gz".format(search_pattern)
            if call(gzip_command.split()) != 0:
                return ErrorCodes.ERRFILENOTFOUND

        elif os.path.isfile(grid_search_pattern):
            return 0


        data_filename = glob(search_pattern)
        try:
            utils.is_file_empty(data_filename)
        except RSTFileEmptyException:
            return ErrorCodes.ERREMPTYFILE

        if 'C.fit' in data_filename:
            data_filename, radar_abbrv = self.convert_fit_to_fitacf(data_filename)

        dmapdump_command = "dmapdump {} | grep -c '\"scan\" = -1'".format(data_filename)
        scan_flag_error = check_output(dmapdump_command,shell=True)

        # Hopefully in the near RST future this situation would be handled more gracefully
        if scan_flag_error != 0:
            grid_options = self.rst_options + "-tl 60 "
        else:
            grid_options = self.rst_options

        if '.a.' in data_filename:
            grid_options = grid_options + " -cn_fix a"
        elif '.b.' in data_filename:
            grid_options = grid_options + " -cn_fix a"
        elif '.c.' in data_filename:
            grid_options = grid_options + " -cn_fix c"
        elif '.d.' in data_filename:
            grid_options = grid_options + " -cn_fix d"
        elif self.parameter['channel'] == 0:
                grid_filename = "{date}.{abbrv}."
                                "grid".format(date=self.parameter["date"])
        elif self.parameter['channel'] == 1:
                grid_filename = "{date}.{abbrv}.a."
                                "grid".format(date=self.parameter["date"])
                grid_options = grid_options + " -cn A"
        elif self.parameter['channel'] == 2:
                grid_filename = "{date}.{abbrv}.b."
                                "grid".format(date=self.parameter["date"])
                grid_options = grid_options + " -cn B"
        else:
            grid_filename = "{date}.{abbrv}."
                                "grid".format(date=self.parameter["date"])
            self.make_grid(grid_filename)
            grid_filename = "{date}.{abbrv}.a."
                                "grid".format(date=self.parameter["date"])
            grid_options = grid_options + " -cn A"
            self.make_grid(grid_filename)
            grid_filename = "{date}.{abbrv}.b."
                                "grid".format(date=self.parameter["date"])
            grid_options = grid_options + " -cn B"
            self.make_grid(grid_filename)
            return 0

        self.make_grid(grid_filename)
        return 0

    def make_grid(self,grid_filename):

            make_grid_command = "make_grid {grid_options} -xtd"
                                " -i {integration_time} -minrng {minrange}"
                                " -vemax {max_velocity}"
                                " > {filename}".format(itegration_time =
                                                       RstConst.INTEGRATION_TIME,
                                                       minrange =
                                                       RstConst.MIN_RANGE,
                                                       max_velocity =
                                                       RstConst.VEMAX,
                                                       filename = grid_filename)

            return_value = call(make_grid_command.split())
            try:
                utils.is_file_not_empty(grid_filename)
            except:
                os.remove(grid_filename)
                return ErrCodes.ERREMPTYFILE

            if return_value != 0:
                return ErrCodes.ERRRST

            return 0

    # TODO: might be a util method
    def convert_fit_to_fitacf(self,filename):
        """
        Converts fit data to fitacf with the standard naming convention used for superDARN data.
        Retruns the fitacf filename that the fit data was saved to and the radar abbrevation associated to the letter.
        """
        match = re.search(r'([a-z])',filename)
        radar_letter = match.group()
        if self.parameter['hemisphere'] == 'south':
            radar_abbrv = SouthRadar.SINGLE_TO_ABBRV[radar_letter]
        else:
            radar_abbrv = NorthRadar.SINGLE_TO_ABBRV[radar_letter]

        fitacf_filename = "{date}.C0.{abbrv}."
                          "fitacf".format(date = self.parameter['date'],
                                          abbrv = radar_abbrv)
        fittofitacf_command = "fittofitacf {filename} >"
                              " {fitacf_filename}".format(filename = filename,
                                                          fitacf_filename =
                                                          fitacf_filename)
        return_value = call(fittofitacf_command.split())
        if return_value != 0:
            raise RSTException('fittofitacf',return_value)

        return (fitacf_filename, radar_abbrv)



    def generate_grid_files(self):
        os.chdir(self.parameter['plotpath'])
        if self.parameter['hemisphere'] == 'south':
            if self.parameter['channel'] == 0:
                radar_list = SouthRadar.SINGLE_EXTENSIONS + \
                             SouthRadar.ABBRV_EXTENSIONS
            elif self.parameter['channel'] == 1:
                radar_list = SouthRadar.SINGLE_EXTENSIONS + \
                             SouthRadar.ABBRV_EXTENSIONS  + \
                             SouthRadar.CHANNEL_ONE_EXTENSIONS
            elif self.parameter['channel'] == 1:
                radar_list = SouthRadar.SINGLE_EXTENSIONS + \
                             SouthRadar.ABBRV_EXTENSIONS  + \
                             SouthRadar.CHANNEL_TWO_EXTENSIONS
            elif self.parameter['channel'] == 3:
                radar_list = SouthRadar.CHANNEL_THREE_EXTENSIONS

            elif self.patamter['channel'] == 4:
                radar_list = NorthRadar.CHANNEL_FOUR_EXTENSIONS
            else:
                radar_list = SouthRadar.SINGLE_EXTENSIONS + \
                             SouthRadar.ABBRV_EXTENSIONS  + \
                             SouthRadar.CHANNEL_ONE_EXTENSIONS + \
                             SouthRadar.CHANNEL_TWO_EXTENSIONS + \
                             SouthRadar.CHANNEL_THREE_EXTENSIONS + \
                             SouthRadar.CHANNEL_FOUR_EXTENSIONS
        elif:
            if self.parameter['channel'] == 0:
                radar_list = NorthRadar.SINGLE_EXTENSIONS + \
                             NorthRadar.ABBRV_EXTENSIONS
            elif self.parameter['channel'] == 1:
                radar_list = NorthRadar.SINGLE_EXTENSIONS + \
                             NorthRadar.ABBRV_EXTENSIONS  + \
                             NorthRadar.CHANNEL_ONE_EXTENSIONS
            elif self.parameter['channel'] == 1:
                radar_list = NorthRadar.SINGLE_EXTENSIONS + \
                             NorthRadar.ABBRV_EXTENSIONS  + \
                             NorthRadar.CHANNEL_TWO_EXTENSIONS
            elif self.parameter['channel'] == 3:
                radar_list = NorthRadar.CHANNEL_THREE_EXTENSIONS

            elif self.patamter['channel'] == 4:
                radar_list = NorthRadar.CHANNEL_FOUR_EXTENSIONS
            else:
                radar_list = NorthRadar.SINGLE_EXTENSIONS + \
                             NorthRadar.ABBRV_EXTENSIONS  + \
                             NorthRadar.CHANNEL_ONE_EXTENSIONS + \
                             NorthRadar.CHANNEL_TWO_EXTENSIONS + \
                             NorthRadar.CHANNEL_THREE_EXTENSIONS + \
                             NorthRadar.CHANNEL_FOUR_EXTENSIONS

        for radar_ext in radar_list:
            self._generate_radar_grid_file(radar_ext)

        combine_grid_command = "combine_grid {options} {date}.*.grid >"
                               "{date}.grd".format(options = self.rst_options,
                                                   date = self.parameter['date'])
        return_value = call(combine_grid_command.split)
        if return_value != 0:
            raise RSTException('combine_grid',return_value)
        utils.is_file_not_empty("{date}.grd".format(self.parameter['date']))


    def generate_map_files(self):
        pass

    def generate_plot_files(self):
        pass

    def cleanup(self):


