#!/usr/bin/env python

# Copyright 2017 SuperDARN Canada
#
# Marina Schmidt
#
# fitacf2convectionMap.py
# 2018-01-26

from __future__ import print_function

import logging
import shutil
import os
import argparse
import re

from datetime import datetime
from subprocess import call, check_output, CalledProcessError
from glob import glob

from DARNprocessing.utils.utils import file_exists, check_rst_command

from DARNprocessing.utils.convectionMapConstants import (ErrorCodes,
                                                         NorthRadar,
                                                         SouthRadar,
                                                         CanadianRadar,
                                                         RstConst,
                                                         RadarConst)

from DARNprocessing.utils.convectionMapWarnings import (ConvertWarning,
                                                        OmniFileNotFoundWarning,
                                                        EmptyDataFileWarning,
                                                        FileNotFoundWarning,
                                                        OmniBadDataWarning,
                                                        OmniFileNotGeneratedWarning)

from DARNprocessing.utils.convectionMapExceptions import (NoGridFilesException,
                                                          OmniException,
                                                          RSTException,
                                                          RSTFileEmptyException,
                                                          PathDoesNotExistException)

from DARNprocessing.IMF_scripts.omni import Omni


class ConvectionMaps():
    """
    Convection Maps is a python class the wraps around the RST commands to generate the following files:
        - grid files
        - map files
        - convection potential plots

    WARNING! Does take in fit files, please makes sure your data is one of the following types:
            - fitacf
            - lmfit2

    If you are using fit files, please read fit2fitacf, generate_fitacf_files or generate_lmfit2_files.
    """

    def __init__(self, arguements=None, parameters=None):
        """
        Reads in user command line options and parses them to correct member
        fields.

        :param sys.args from command line
        :param Dictionary of the command line arguements; used for testing and python scripts
                key name: defualt value
                -----------------------
                'date': None,
                'channel': 5,
                'hemisphere': 'north',
                'canadian': False,
                'start_time': '00:00',
                'end_time': 23:59,
                'image_extension': 'pdf',
                'integration_time': 120,
                'datapath': self._current_path,
                'plotpath': self._current_path,
                'omnipath': self._current_path,
                'mappath': self._current_path,
                'keypath': self._current_path,
                'num_proc': 1
        """
        self._current_date = datetime.now()
        self._current_path = os.getcwd()

        if not parameters:
            self.arguement_parser(arguements)
        else:
            self.parameter = {'date': None,
                              'channel': 5,
                              'integration_time':120,
                              'hemisphere': 'north',
                              'start_time': '00:00',
                              'end_time': '23:59',
                              'rst_version': 4.1,
                              'image_extension': 'pdf',
                              'logfile': self._current_path+'/ConvectionMaps.log',
                              'datapath': self._current_path,
                              'plotpath': self._current_path,
                              'omnipath': self._current_path,
                              'mappath': self._current_path,
                              'keypath': self._current_path,
                              'num_proc': 1}

            self.parameter.update(parameters)
            if not self.parameter['date']:
                raise ValueError("Date of the date was not passed in, please"
                                 "include in the parameters dictionary")

        # the possible letter channels that a fit file name can contain
        # that pertains to the stero channel value. Most used by alaskian radars.
        self.channel = ['', 'a', 'b', 'c', 'd']

        # Logging information setup
        # TODO: give a defualt directory to store the files in?
        FORMAT = "%(levelname)s %(asctime)-15s: %(message)s"
        logging.basicConfig(filename=self.parameter['logfile'],
                            format=FORMAT,
                            level=logging.DEBUG)
        logging.info("Parameter list:" + str(self.parameter))
        self._generate_paths()
        # TODO clean up rst options and make it a requirement to use only rst 4.0 and higher
        self.rst_options = ""
        self.radars_used = "Radar files uses in the Convection Map process:\n"
        self.radars_missing = "Radar files missing"\
                              " (not used in the Convection Map process):\n"
        self.radars_errors = "Radars files that raised errors:\n"

    # TODO: Should this be utils?
    # TODO: Look for more possible options to add here for changing convection maps
    def arguement_parser(self, arguements):
        """
        Arguement parser - parses the arguement passed into the script into a
                    parameter dictionary.
        Parameters
        ----------
        arguements - sys.args
        """
        parser = argparse.ArgumentParser(prog='fitacf2convectionmap',
                                         description='Converts fitacf files'
                                                     ' to convection maps')
        # required arguement
        parser.add_argument('date', type=str,
                            help='The date of the fitacf data.'
                            ' Format: YYYYMMDD')

        # RST options
        parser.add_argument('-c', '--channel', type=str,
                            choices=[0, 1, 2, 3, 4, 5], default='5',
                            help='Select the channel number of data'
                            ' to use for the convection map process.'
                            ' Default: 5 - use all channels')
        parser.add_argument('--integration-time', type=int,
                            default='120',
                            help='Integration time between each plot in seconds.'
                            ' Default: 120 - 2 minute convection plots')
        parser.add_argument('--hemisphere', type=str,
                            choices=['north', 'south'], default='north',
                            help='The hemisphere you want to assimilate.'
                            ' Default: north')
        parser.add_argument('--canadian', action='store_true',
                            help='Set to use only the canadian radards.')
        parser.add_argument('--start-time', type=str,
                            metavar='hh:mm', default='00:00',
                            help='The start time at hh:mm of the fitacf data.'
                            ' Default: 00:00')
        parser.add_argument('--end-time', type=str,
                            metavar='hh:mm', default='23:59',
                            help='The end time at hh:mm of the fitacf data.'
                            ' Default: 23:59')
        parser.add_argument('--rst-version', type=float,
                            metavar='N', default=4.1,
                            help='The version number of RST that'
                            ' you are using. Default: 4.1')
        parser.add_argument('-i', '--image-extension', type=str,
                            metavar='EXTENSION', default='pdf',
                            help='The image format of convection maps.'
                            ' Default: pdf')

        # This was going to be used in the case of a general script, however,
        # I am currently not sure which steps are needed for various data
        # formats and in the future it might be easier for the user to
        # to inherit this class and then modify as needed for the format.
        # TODO: decide whether this should be taken out.
        # parser.add_argument('-f','--data-format',type=str,
        #                    choices=['fitacf','fit','fitred'],default='fitacf ',
        #                    help='The data format to use for generating the'
        #                    ' convection maps Default: fitacf')

        # Path options
        parser.add_argument('-l', '--logfile', type=str,
                            metavar='PATH',
                            default=self._current_path+'/ConvectionMaps.log',
                            help='The absolute path to the log file'
                            ' Default: {}/ConvectionMaps.log'
                            ''.format(self._current_path))

        parser.add_argument('-d', '--datapath', type=str,
                            metavar='PATH', default=self._current_path,
                            help='The absolute path to the fitacf data.'
                            ' Default: {}'.format(self._current_path))
        parser.add_argument('-p', '--plotpath', type=str,
                            metavar='PATH', default=self._current_path,
                            help='The absolute path to where the convection'
                            ' maps will be saved.'
                            ' Default: {}'.format(self._current_path))
        parser.add_argument('-o', '--omnipath', type=str,
                            metavar='PATH', default=self._current_path,
                            help='The absolute path to where the omni files'
                            ' will be saved to.'
                            ' Default: {}'.format(self._current_path))
        parser.add_argument('-m', '--mappath', type=str,
                            metavar='PATH', default=self._current_path,
                            help='The absolute path to where the map files'
                            ' will be saved to.'
                            ' Default: {}'.format(self._current_path))
        parser.add_argument('-k', '--keypath', type=str,
                            metavar='PATH', default=self._current_path,
                            help="The absolute path to the key file for"
                            "the convection maps."
                            " Default: {}".format(self._current_path))

        # Parallel options
        parser.add_argument('-n', '--num_proc', type=int,
                            metavar='NUMPROCESSORS', default=1,
                            help='The number of processors you wish to use'
                            ' in parallel mode. '
                            ' This option enables parallel mode.'
                            ' Not implemented yet'
                            ' Default: 1')

        # Standard options, note: the help option is handled by argparse
        parser.add_argument('-v', '--verbose', action='store_true',
                            help='Turns on verbose mode.')

        self.parameter = parser.parse_args()
        self.parameter = vars(self.parameter)
        print(self.parameter)
        if not os.path.exists(self.parameter['datapath']):
            raise PathDoesNotExistException(self.parameter['datapath'])

    def set_datapath(self, new_datapath):
        self.parameter['datapath'] = new_datapath
        if not os.path.exists(self.parameter['datapath']):
            raise PathDoesNotExistException(self.parameter['datapath'])

    def _generate_paths(self):
        """
        generate the folder paths for the various data storage
        """
        # creates the paths if they are not already created.
        if not os.path.exists(self.parameter['datapath']):
            raise PathDoesNotExistException(self.parameter['datapath'])

        for path in [self.parameter['plotpath'],
                     self.parameter['omnipath'],
                     self.parameter['mappath']]:
            try:
                os.makedirs(path)
            except OSError as err:
                # errno code for file exists
                if err.errno == 17:
                    continue
                else:
                    raise OSError(err)

        logging.info("The following data files will be"
                     " stored in the following paths")
        logging.info("Plot path: " + self.parameter['plotpath'])
        logging.info("Map files path: " + self.parameter['mappath'])
        logging.info("Omni file path: " + self.parameter['omnipath'])
        logging.info("The data for the convections maps is obtained from")
        logging.info("Data path: " + self.parameter['datapath'])

    # TODO: implement parallel version
    def _generate_radar_grid_file(self, radar_abbrv, data_path):
        """
        Helper function for generate_grid_files to generate a grid file(s) for
        a single radar extension. This can be used to parallelize the grid
        generation process.
        """
        # TODO: delete it if glob works for getting any type of file name
        # data_filename = "{date}{ext}".format(date=self.parameter['date'],
        #                                      ext=radar_ext)

        data_filename = os.path.basename(data_path)

        # Standard naming convention for grid files
        grid_filename = "{date}.{abbrv}.grid".format(date=self.parameter['date'],
                                                     abbrv=radar_abbrv)

        grid_path = "{datapath}/{grid_file}"\
                    "".format(datapath=self.parameter['plotpath'],
                              grid_file=grid_filename)

        # if the data file is not in the current file then check in the
        # in the provided data folder.
        if os.path.isfile(data_path):
            try:
                shutil.copy2(data_path,
                             self.parameter['plotpath']+'/'+data_filename)
            except shutil.Error as msg:
                logging.warn(msg)

            data_path = self.parameter['plotpath']+'/'+data_filename

            # unzip any possible compression formats...
            # TODO: replace this with a dictionary to key in for various compression types
            #       and the dictionary lives in the constants file so that the user changes that file
            #       not this file
            if 'gz' in data_path:
                gzip_command = "gzip -df {datapath}"\
                               "".format(datapath=data_path,
                                         plotpath=self.parameter['plotpath'])
                if call(gzip_command, shell=True) != 0:
                    logging.warn(FileNotFoundWarning(data_filename))
                    self.radars_errors += data_filename + '\n'
                    return ErrorCodes.ERRFILENOTFOUND
                data_filename = data_filename.strip('.gz')

            elif 'bz2' in data_path:
                bzip2_command = "bzip2 -dfv {datapath}"\
                                "".format(datapath=data_path,
                                          plotpath=self.parameter['plotpath'])
                if call(bzip2_command, shell=True) != 0:
                    logging.warn(FileNotFoundWarning(data_filename))
                    self.radars_errors += data_filename + '\n'
                    return ErrorCodes.ERRFILENOTFOUND
                data_filename = data_filename.strip('.bz2')

        else:
            logging.warn("{datafile} was not found in the datapath: {datapath}"
                         " or plotpath: {plotpath}, this file will not be used"
                         "in the convection map process"
                         "".format(datapath=self.parameter['datapath'],
                                   datafile=data_filename,
                                   plotpath=self.parameter['plotpath']))
            self.radars_missing += data_filename + '\n'
            message = "File {datafile} was not found, please make sure to"\
                      " provide data path using -d option and that the"\
                      " file exist in the folder"
            raise OSError(message)

        data_path = self.parameter['plotpath']+'/'+data_filename

        if os.path.getsize(data_path) == 0:
            logging.warn(EmptyDataFileWarning(data_filename))
            self.radars_errors += data_filename + '\n'
            return ErrorCodes.ERREMPTYFILE

        # TODO: maybe remove fit checking and make it a requirement and write a wrapper to convert fit files.
        #       this is a hassel to check :( and really we should just archive fit files and convert to the most current file type
        if 'C.fit' in data_filename:
            try:
                data_path, radar_abbrv = self.convert_fit_to_fitacf(data_path)
            except RSTException as err:
                logging.exception(err)
                return ErrorCodes.ERRRST

        dmapdump_command = "dmapdump {} | grep -c '\"scan\" = -1'"\
                           "".format(data_path)

        grid_options = self.rst_options + ' -i ' + \
            str(self.parameter['integration_time'])

        # We need this try/except block because grep will return a non-zero
        # exit value even if there is no error, example) if there is no match
        # it will return 1
        # check_output will throw an exception on non-zero return values
        try:
            neg_scan_flag = check_output(dmapdump_command, shell=True)
        except CalledProcessError as e:
            neg_scan_flag = e.output  # Gets the output of the command
        # Hopefully in the near RST future this situation
        # would be handled more gracefully
        if int(neg_scan_flag) > 0:
            # TODO: this may not be needed in the newest version of RST
            grid_options += "-tl 60 "

        channelA = self._check_for_channel(data_path, 1)
        channelB = self._check_for_channel(data_path, 2)
        monochannel = self._check_for_channel(data_path, 0)

        data_filename = os.path.basename(data_path)
        if '.a.' in data_filename:
            grid_options = grid_options + " -cn_fix a"
        elif '.b.' in data_filename:
            grid_options = grid_options + " -cn_fix a"
        elif '.c.' in data_filename:
            grid_options = grid_options + " -cn_fix c"
        elif '.d.' in data_filename:
            grid_options = grid_options + " -cn_fix d"
        elif self.parameter['channel'] == 0:
                grid_path = "{plotpath}/{date}.{abbrv}."\
                            "grid".format(date=self.parameter["date"],
                                          plotpath=self.parameter['plotpath'],
                                          abbrv=radar_abbrv)
        elif self.parameter['channel'] == 1:
                grid_path = "{plotpath}/{date}.{abbrv}.a."\
                            "grid".format(date=self.parameter["date"],
                                          plotpath=self.parameter['plotpath'],
                                          abbrv=radar_abbrv)
                grid_options = grid_options + " -cn A"
        elif self.parameter['channel'] == 2:
                grid_path = "{plotpath}/{date}.{abbrv}.b."\
                            "grid".format(date=self.parameter["date"],
                                          plotpath=self.parameter['plotpath'],
                                          abbrv=radar_abbrv)
                grid_options = grid_options + " -cn B"
        else:
            if monochannel > 0:
                grid_path = "{plotpath}/{date}.{abbrv}."\
                            "grid".format(date=self.parameter["date"],
                                          plotpath=self.parameter['plotpath'],
                                          abbrv=radar_abbrv)
                self.make_grid(data_path, grid_path, grid_options)

            if channelA > 0:
                grid_path = "{plotpath}/{date}.{abbrv}.a."\
                            "grid".format(date=self.parameter["date"],
                                          plotpath=self.parameter['plotpath'],
                                          abbrv=radar_abbrv)
                grid_optionsA = grid_options + " -cn A"
                self.make_grid(data_path, grid_path, grid_optionsA)

            if channelB > 0:
                grid_path = "{plotpath}/{date}.{abbrv}.b."\
                            "grid".format(date=self.parameter["date"],
                                          plotpath=self.parameter['plotpath'],
                                          abbrv=radar_abbrv)
                grid_optionsB = grid_options + " -cn B"
                self.make_grid(data_path, grid_path, grid_optionsB)
            return 0

        self.make_grid(data_path, grid_path, grid_options)
        return 0

    # Maybe move this function to utils?
    def _check_for_channel(self, data_file, channel_num):
        """
        A method to check for the channel number in a fitacf file
        that may use mono and stero.
        """
        channel_command = "dmapdump {filename} "\
                          "| grep -c '\"channel\" = {channel}'"\
                          "".format(filename=data_file,
                                    channel=channel_num)
        try:
            channel_count = check_output(channel_command, shell=True)
        except CalledProcessError as e:
            channel_count = e.output  # Gets the output of the command
        return int(channel_count)

    def make_grid(self, data_file, grid_file, grid_options=""):
        make_grid_command = "make_grid {gridoptions} -xtd"\
                            " -i {integration_time} -minrng 2"\
                            " -vemax {max_velocity}"\
                            " {datafile} > {gridpath}"\
                            "".format(gridoptions=grid_options,
                                      integration_time=RstConst.INTEGRATION_TIME,
                                      max_velocity=RstConst.VEMAX,
                                      datafile=data_file,
                                      gridpath=grid_file)

        logging.info(make_grid_command)
        try:
            check_rst_command(make_grid_command, grid_file)
        except RSTException as err:
            logging.warn(err)
            self.radars_errors += data_file + '\n'
        except RSTFileEmptyException as err:
            self.radars_errors += data_file + '\n'
            logging.warn(err)
            os.remove(grid_file)

    # TODO: might be a util method
    def convert_fit_to_fitacf(self, file_path):
        """
        Converts fit data to fitacf with the standard naming convention used for
        superDARN data.
        Retruns the fitacf filename that the fit data was saved to and the radar
        abbrevation associated to the letter.
        """
        match = re.search(r'([a-z])', os.path.basename(file_path))
        radar_letter = match.group()
        if self.parameter['hemisphere'] == 'south':
            radar_abbrv = SouthRadar.SINGLE_TO_ABBRV[radar_letter]
        else:
            radar_abbrv = NorthRadar.SINGLE_TO_ABBRV[radar_letter]

        fitacf_path = "{plotpath}/{date}.C0.{abbrv}."\
                      "fitacf".format(date=self.parameter['date'],
                                      abbrv=radar_abbrv,
                                      plotpath=self.parameter['plotpath'])
        fittofitacf_command = "fittofitacf {filepath} >"\
                              " {fitacf_filename}"\
                              "".format(filepath=file_path,
                                        fitacf_filename=fitacf_path)
        check_rst_command(fittofitacf_command, fitacf_path)

        return (fitacf_path, radar_abbrv)

    # TODO: need to determine what wrappers should be where ... hmmm

    # TODO: implement a method to generate fitacf files from rawacf files
    def generate_fitacf_files(self):
        pass

    # TODO: implement a method to convert rawacf to lmfit using Ashton's code
    def generate_lmfit_files(self):
        pass

    def concatinate_fitted_date(self):
        pass

    def generate_grid_files(self):
        """
        Generates the grid files used in the map generation step.
        """
        radar_abbrv = []
        if self.parameter['hemisphere'] == 'south':
            radar_abbrv = SouthRadar.RADAR_ABBRV
        elif self.parameter['hemisphere'] == 'canadian':
            radar_abbrv = CanadianRadar.RADAR_ABBRV
        else:
            radar_abbrv = NorthRadar.RADAR_ABBRV

        # TODO: need to handle fit files...
        grid_file_counter = 0
        for ext in RadarConst.FILE_TYPE:
            for abbrv in radar_abbrv:
                file_pattern = "{datapath}/{date}*{abbrv}*.{ext}*"\
                               "".format(datapath=self.parameter['datapath'],
                                         date=self.parameter['date'],
                                         abbrv=abbrv,
                                         ext=ext)
                for filename in glob(file_pattern):
                    if self._generate_radar_grid_file(abbrv, filename) == 0:
                        grid_file_counter += 1

        logging.info(self.radars_used)
        logging.info(self.radars_missing)
        logging.info(self.radars_errors)

        if grid_file_counter == 0:
            logging.error(NoGridFilesException)
            raise NoGridFilesException

        grd_filename = "{date}.grd".format(date=self.parameter['date'])
        grd_path = "{plotpath}/{grd_file}"\
                   "".format(plotpath=self.parameter['plotpath'],
                             grd_file=grd_filename)

        combine_grid_command = "combine_grid {options} {plotpath}/{date}.*.grid"\
                               " > {grdpath}"\
                               "".format(options=self.rst_options,
                                         plotpath=self.parameter['plotpath'],
                                         date=self.parameter['date'],
                                         grdpath=grd_path)

        check_rst_command(combine_grid_command, grd_path)

    def generate_map_files(self):
        """
        Generates the various map files for the radar fit/fitacf files availible for
        the given date and hemisphere. The 'date.map' is the only saved file,
        the other map files are removed at the end of the convection process.
        """
        map_grd_options = ""

        if self.parameter['hemisphere'] == "south":
            map_grd_options = self.rst_options + " -sh"

        grd_path = "{plotpath}/{date}.grd"\
                   "".format(plotpath=self.parameter['plotpath'],
                             date=self.parameter['date'])
        file_exists(grd_path)
        empty_map_filename = "{date}.empty.map"\
                             "".format(date=self.parameter['date'])
        empty_map_path = "{plotpath}/{empty_map}"\
                         "".format(plotpath=self.parameter['plotpath'],
                                   empty_map=empty_map_filename)

        map_grd_command = "map_grd {options} -l 50 {plotpath}/{date}.grd > "\
                          "{plotpath}/{filename}"\
                          "".format(options=map_grd_options,
                                    plotpath=self.parameter['plotpath'],
                                    date=self.parameter['date'],
                                    filename=empty_map_filename)\

        check_rst_command(map_grd_command, empty_map_path)

        hmb_map_filename = "{date}.hmb.map".format(date=self.parameter['date'])
        hmb_map_path = "{plotpath}/{hmb_map}"\
                       "".format(plotpath=self.parameter['plotpath'],
                                 hmb_map=hmb_map_filename)

        map_addhmb_command = "map_addhmb {options} {plotpath}/{empty_map} >"\
                             " {plotpath}/{hmb_map}"\
                             "".format(options=self.rst_options,
                                       plotpath=self.parameter['plotpath'],
                                       empty_map=empty_map_filename,
                                       hmb_map=hmb_map_filename)

        check_rst_command(map_addhmb_command, hmb_map_path)

        omni = Omni(self.parameter['date'], self.parameter['omnipath'])

        try:
            update = omni.check_for_updates()
            if update:
                old_omni_file = "{omnipath}/{date}_omni_{currentdate}.txt"\
                                "".format(date=self.parameter['date'],
                                          currentdate=self._current_date.strftime("%Y%m%d"))
                try:
                    shutil.move(omni.omni_path, old_omni_file)
                except IOError as err:
                    logging.exception(err)
                    pass
        except OmniFileNotFoundWarning as warning_msg:
            logging.warn(warning_msg)
            update = True

        try:
            if update:
                omni.get_omni_file()

            omni.omnifile_to_IMFfile()

            imf_map_filename = "{date}.imf.map"\
                               "".format(date=self.parameter['date'])
            imf_map_path = "{omnipath}/{imf_map}"\
                           "".format(omnipath=self.parameter['omnipath'],
                                     imf_map=imf_map_filename)

            map_addimf_command = "map_addimf {options} -omni -d 00:10"\
                                 " -if {omnipath}/{imf_filename}"\
                                 " {plotpath}/{hmb_map} >"\
                                 " {plotpath}/{imf_map}"\
                                 "".format(options=self.rst_options,
                                           omnipath=self.parameter['omnipath'],
                                           plotpath=self.parameter['plotpath'],
                                           imf_filename=omni.imf_filename,
                                           hmb_map=hmb_map_filename,
                                           imf_map=imf_map_filename)

            check_rst_command(map_addimf_command, imf_map_path)
            self._imf_option = " -imf"
            input_model_file = imf_map_filename

        except OmniException as err_msg:
            logging.error(err_msg)
            self._imf_option = ""
            input_model_file = hmb_map_filename

        except (OmniFileNotGeneratedWarning,
                OmniFileNotFoundWarning,
                OmniBadDataWarning) \
                as warning_msg:
            logging.warn(warning_msg)
            self._imf_option = ""
            input_model_file = hmb_map_filename

        map_model_filename = "{date}.model.map"\
                             "".format(date=self.parameter['date'])
        map_model_path = "{plotpath}/{map_model}"\
                         "".format(plotpath=self.parameter['plotpath'],
                                   map_model=map_model_filename)

        map_addmodel_command = "map_addmodel {options} -o 8 -d l "\
                               "{plotpath}/{input_map} > {plotpath}/{model_map}"\
                               "".format(options=self.rst_options,
                                         plotpath=self.parameter['plotpath'],
                                         input_map=input_model_file,
                                         model_map=map_model_filename)
        check_rst_command(map_addmodel_command, map_model_path)

        map_filename = "{date}.map".format(date=self.parameter['date'])
        map_path = "{plotpath}/{map_file}"\
                   "".format(plotpath=self.parameter['plotpath'],
                             map_file=map_filename)

        map_fit_command = "map_fit {options} {plotpath}/{model_map} >"\
                          " {plotpath}/{map_file}"\
                          "".format(options=self.rst_options,
                                    plotpath=self.parameter['plotpath'],
                                    model_map=map_model_filename,
                                    map_file=map_filename)
        check_rst_command(map_fit_command, map_path)
        try:
            shutil.copy2(map_path, self.parameter["mappath"])
        except shutil.Error:
            pass

    def generate_RST_convection_maps(self):
        """
        Generates the convection maps using the RST map_plot function.
        """

        logging.info("Generating Convection Maps uring RST ")
        # TODO: A better method of importing the key file and
        # what to do when it is not provided
        shutil.copy2("{}/rainbow.key".format(self.parameter['keypath']), self.parameter['plotpath'])
        key_option = "-vkeyp -vkey_path {}/ -vkey rainbow.key"\
                     "".format(self.parameter['plotpath'])
        map_path = "{mappath}/{date}.map"\
                   "".format(mappath=self.parameter['mappath'],
                             date=self.parameter['date'])

        post_script_path = "{}/*.ps".format(self.parameter['plotpath'])
        file_exists(map_path)
        map_plot_command = "map_plot {options} -ps -mag"\
                           " -st {start_time} -et {end_time} -rotate -hmb -modn"\
                           " -fit -grd -ctr {imf} -dn -extra -coast -vecp "\
                           " -pot -time {key} -path {plotpath} {mappath}"\
                           " 2>/dev/null"\
                           "".format(options=self.rst_options,
                                     start_time=self.parameter['start_time'],
                                     end_time=self.parameter['end_time'],
                                     imf=self._imf_option,
                                     key=key_option,
                                     plotpath=self.parameter['plotpath'],
                                     mappath=map_path)
        logging.info(map_plot_command)
        check_rst_command(map_plot_command, post_script_path)

        for ps_file in glob(post_script_path):
            image_filename = ps_file.replace(".ps", "")
            convert_command = "convert -density 200 {ps_filename} "\
                              " {filename}.{ext}"\
                              "".format(plotpath=self.parameter['plotpath'],
                                        ps_filename=ps_file,
                                        filename=image_filename,
                                        ext=self.parameter['image_extension'])
            return_value = call(convert_command.split())
            if return_value != 0:
                logging.warn(ConvertWarning(ps_file,
                                            self.parameter['image_extension']))

    def cleanup(self):
        """
        Cleans up any meta or data that should not be stored in the plot path.
        """
        path = "{plotpath}/{date}".format(plotpath=self.parameter['plotpath'],
                                          date=self.parameter['date'])

        for f in glob(path+'*.grid'):
            os.remove(f)
        for f in glob(path+'*.map'):
            os.remove(f)
        for ext in RadarConst.FILE_TYPE:
            for f in glob('{path}*.{ext}*'.format(path=path, ext=ext)):
                os.remove(f)
        os.remove(path + ".grd")


if __name__ == '__main__':
    import sys
    convec = ConvectionMaps(sys.argv[1:], 201803)
    # convec.setup_paths()
    convec.generate_grid_files()
    convec.generate_map_files()
    convec.generate_RST_convection_maps()
