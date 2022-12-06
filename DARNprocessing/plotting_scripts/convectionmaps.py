#!/usr/bin/env python

# Copyright 2017 SuperDARN Canada
#
# Author: Marina Schmidt
# Date: 2018-01-26
#
# Modifications:
# 20221129 : CJM : Updates and review comments


from __future__ import print_function

import logging
import shutil
import os
import subprocess as sp
import re

from datetime import datetime
from glob import glob

from DARNprocessing.utils.utils import (file_exists,
                                        check_rst_command,
                                        parse_command_line_args,
                                        path_exists)

from DARNprocessing.utils.convectionMapConstants import (NorthRadar,
                                                         SouthRadar,
                                                         RstConst,
                                                         FileConst)

from DARNprocessing.utils.convectionMapWarnings import (ConvertWarning,
                                                        OmniFileNotFoundWarning,
                                                        EmptyDataFileWarning,
                                                        OmniBadDataWarning,
                                                        OmniFileNotGeneratedWarning)

from DARNprocessing.utils.convectionMapExceptions import (NoGridFilesException,
                                                          OmniException,
                                                          RSTException,
                                                          FileDoesNotExistException,
                                                          RSTFileEmptyException,
                                                          PathDoesNotExistException,
                                                          UnsupportedTypeException)

from DARNprocessing.IMF_scripts.omni import Omni


class ConvectionMaps():
    """
    Convection Maps is a python class the wraps around the RST commands to
    generate the following files:
        - grid files
        - map files
        - convection potential plots

    WARNING! Does not take in fit files, please makes sure your data is one
    of the following types:
            - fitacf
            - lmfit2

    If you are using fit files, please read fit2fitacf, generate_fitacf_files or
    generate_lmfit2_files.
    * Currently not implemented *
    """

    def __init__(self, arguments=None, parameters=None):
        """
        Reads in user command line options and parses them to correct member
        fields.

        :param arguments: sys.args from command line
        :param parameters: Dictionary of the command line arguements; used for testing or
               python scripts
                key name: default value
                -----------------------
                'date': None,
                'channel': 5,
                'hemisphere': 'north',
                'start_time': '00:00',
                'end_time': 23:59,
                'image_ext': 'pdf',
                'integration_time': 120, in seconds
                'data_path': self._current_path,
                'plot_path': self._current_path,
                'map_path': self._current_path,
                'grid_path': self._current_path,
                'imf_path': self._current_path,
                'key_path': self._current_path,
                'num_proc': 1

        :raise ValueError: date parameter is required

        """

        self._current_date = datetime.now()
        self._current_path = os.getcwd()

        # If the parameters are read in from a python program, use those
        # If there are no parameters but arguments are read in from
        # command line, convert those to parameters dictionary
        # If there are parameters read in, make sure they're all there
        # and use the defaults if not
        if not parameters:
            self.create_command_line_args(arguments)
        else:
            # Default values
            self.parameter = {'date': None,
                              'channel': '',
                              'integration_time': 120,
                              'hemisphere': 'north',
                              'start_time': '00:00',
                              'end_time': '23:59',
                              'image_ext': 'pdf',
                              'logpath': self._current_path,
                              'data_path': self._current_path,
                              'plot_path': self._current_path,
                              'map_path': self._current_path,
                              'grid_path': self._current_path,
                              'imf_path': self._current_path,
                              'key_path': self._current_path,
                              'num_proc': 1}

            # Get defaults and then update with any new parameters read in
            self.parameter.update(parameters)
            # Date is the only required field
            if self.parameter['date'] is None:
                raise ValueError("Date was not passed in, please"
                                 "include in the parameters dictionary")

        # Convert the hemisphere to char and correct parameter
        if self.parameter['hemisphere'] == 'north':
            hemisphere_identifier = 'n'
            self.hem_ext = 'n'
        elif self.parameter['hemisphere'] == 'south':
            hemisphere_identifier = 's'
            self.hem_ext = 's'

        # Set log file path
        self.parameter.update({'logfile':
                               '{path}/{date}_map.{hemisphere}.log'
                               .format(path=self.parameter['logpath'],
                                       date=self.parameter['date'],
                                       hemisphere=hemisphere_identifier)})

        # Check if the data path exists
        path_exists(self.parameter['data_path'])

        # Possible letters used for channel names - TODO: allow any char
        # Does this line need to be included?
        self.channel = ['', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']

        # Logging information setup
        FORMAT = "%(levelname)s %(asctime)s: %(message)s"
        logging.basicConfig(filename=self.parameter['logfile'],
                            format=FORMAT,
                            level=logging.DEBUG)
        # Log parameters used to make map files
        logging.info("Parameter list:" + str(self.parameter))

        # Generate map path and plot path if they do not exist, log what paths
        # are being used
        self._generate_paths()

        # TODO: not be hardcoded if special rst options are needed
        self.rst_options = ""

        # Logging information on radars used, and radars that gave errors
        # Not logged here, logged later with additions
        self.radars_used = "***Radar files used in production:***\n"
        self.radars_errors = "***Radars files that raised errors:***\n"


    def create_command_line_args(self, arguments):
        """
        Argument parser - parses the argument passed into the script into a
                    parameter dictionary. Used when called from command line.

            :param arguments: sys.args
        """
        # Note: -h is reserved for --help so -H for hemisphere
        option_names = [('date'),
                        ('-c', '--channel'),
                        ('-i', '--integration-time'),
                        ('-H', '--hemisphere'),
                        ('-s', '--start-time'),
                        ('-e', '--end-time'),
                        ('-x', '--image-ext'),
                        ('-l', '--logpath'),
                        ('-d', '--data-path'),
                        ('-f', '--imf-path'),
                        ('-p', '--plot-path'),
                        ('-m', '--map-path'),
                        ('-g', '--grid-path'),
                        ('-k', '--key-path'),
                        ('-v', '--verbose')]
        # Sets Defaults if option not used
        option_settings = [{'type': str,
                            'metavar': 'YYYYMMDD',
                            'help': 'The date of the fitacf data.'},
                           {'type': str,
                            'choices': ['', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'],
                            'default': '',
                            'help': 'Select the channel letter. Either a'
                            ' single character e.g. "a" to use for'
                            ' the convection map process.'
                            ' Default: '' - use all channels'},
                           {'type': int,
                            'default': '120',
                            'help': 'Integration time between each plot in seconds.'
                            ' Default: 120 - 2 minute convection plots'},
                           {'type': str,
                            'choices': ['north', 'south'],
                            'default': 'north',
                            'help': 'The hemisphere you want to assimilate.'
                            ' Default: north'},
                           {'type': str,
                            'metavar': 'hh:mm',
                            'default': '00:00',
                            'help': 'The start time at hh:mm of the fitacf data.'
                            ' Default: 00:00'},
                           {'type': str,
                            'metavar': 'hh:mm',
                            'default': '23:59',
                            'help': 'The end time at hh:mm of the fitacf data.'
                            ' Default: 23:59'},
                           {'type': str,
                            'metavar': 'EXTENSION',
                            'default': 'png',
                            'help': 'The image format of convection maps.'
                            ' Default: pdf'},
                           {'type': str,
                            'metavar': 'PATH',
                            'default': self._current_path,
                            'help': 'The absolute path where the log file will be saved'
                            ' Default: {}'
                            ''.format(self._current_path)},
                           {'type': str,
                            'metavar': 'PATH',
                            'default': self._current_path,
                            'help': 'The absolute path to the fitacf data.'
                            ' Default: {}'.format(self._current_path)},
                           {'type': str,
                            'metavar': 'PATH',
                            'default': self._current_path,
                            'help': 'The absolute path to the imf data'
                            'default: {}'.format(self._current_path)},
                           {'type': str,
                            'metavar': 'PATH',
                            'default': self._current_path,
                            'help': 'The absolute path to where the convection'
                            ' maps will be saved.'
                            ' Default: {}'.format(self._current_path)},
                           {'type': str,
                            'metavar': 'PATH',
                            'default': self._current_path,
                            'help': 'The absolute path to where the map files'
                            ' will be saved to.'
                            ' Default: {}'.format(self._current_path)},
                           {'type': str,
                            'metavar': 'PATH',
                            'default': self._current_path,
                            'help': 'The absolute path to where the grid files'
                            ' will be saved to.'
                            ' Default: {}'.format(self._current_path)},
                           {'type': str,
                            'metavar': 'PATH',
                            'default': self._current_path,
                            'help': "The absolute path to the key file for"
                            "the convection maps."
                            " Default: {}".format(self._current_path)},
                           {'action': 'store_true',
                            'help': 'Turns on verbose mode.'}]
        self.parameter = parse_command_line_args('convectionmaps',
                                      'Converts fitted data files to convection maps',
                                      option_names,
                                      option_settings)


    def _generate_paths(self):
        """
        Generate the directory paths and log information
        """
        for path in [self.parameter['plot_path'],
                     self.parameter['map_path'],
                     self.parameter['grid_path']]:
            try:
                path_exists(path)
            except PathDoesNotExistException:
                try:
                    os.makedirs(path)
                except OSError as err:
                    logging.info(err)
                    pass


        logging.info("The following data files will be"
                     " stored in the following paths:")
        logging.info("Plot path: " + self.parameter['plot_path'])
        logging.info("Grid path: " + self.parameter['grid_path'])
        logging.info("Map files path: " + self.parameter['map_path'])
        logging.info("Omni files path: " + self.parameter['map_path'])
        logging.info("The data for the convections maps is obtained from")
        logging.info("Data path: " + self.parameter['data_path'])


    def _check_for_channel(self, data_file, channel_char):
        """
        A method to check if a channel exists inside a file rather than in
        separate files. Returns True if channel exists in file, returns
        False if no records with channel found.
        """
        channel_command = "dmapdump {filename} "\
                          "| grep -c '\"channel\" = {channel}'"\
                          "".format(filename=data_file,
                                    channel=channel_char)
        try:
            channel_count = sp.check_output(channel_command, shell=True)
            if channel_count > 0:
                return True
            else:
                return False
        except sp.CalledProcessError:
            return False


    def generate_radar_grid_file(self, radar_abbrv, data_file):
        """
        Helper function for generate_grid_files to generate a grid file(s) for
        a single radar extension. This can be used to parallelize the grid
        generation process.

            :param radar_abbrv: 3 letter acroynm of the radar
            :param data_file: str fitted data file name with full extension
            :raise ValueError: if the radar abbreviation is not in the data file
                               name which means it could be generating the wrong
                               grid file.
        """
        if radar_abbrv not in data_file:
            logging.error('Mismatched radar abbreviation: {radar} and file name'
                          ' {filename}'.format(radar=radar_abbrv,
                                               filename=data_file))
            raise ValueError('Mismatched radar abbreviation: {radar} and file name'
                             ' {filename}'.format(radar=radar_abbrv,
                                                  filename=data_file))

        grid_options = ''
        # Uses standard naming convention for grid files
        grid_filename = "{date}.{abbrv}.{hemisphere}."\
                "grid".format(date=self.parameter['date'],
                              abbrv=radar_abbrv,
                              hemisphere=self.hem_ext)

        grid_path = "{grid_path}/{grid_file}"\
                    "".format(grid_path=self.parameter['grid_path'],
                              grid_file=grid_filename)

        # Set up options in make_grid. -tl ignores scan flag and sets scans at
        # time interval (120 here default for map files)
        grid_options += ' -tl 120 -i ' + str(self.parameter['integration_time'])

        # TODO: Unlimited channels chars?
        # You can choose to use all channels, or a single channel
        # If all channels chosen, iterate over a to h - most wont exist
        # All channels are automatically used in RST so only the output files
        # are amended to state which files used
        if self.parameter['channel'] == '':
            chans = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
            for chan in chans:
                if '.{}.'.format(chan) in data_file:
                    grid_options = grid_options + " -cn_fix {}".format(chan)
                elif self._check_for_channel(data_file, chan):
                    grid_options = grid_options + " -cn_fix {}".format(chan)
        # If a channel is chosen
        elif not self.parameter['channel'] == '':
            # If a separate file for that channel exists
            if '.{}.'.format(chan) in data_file:
                grid_options = grid_options + " -cn {} -cn_fix {}"\
                                    .format(self.parameter['channel'],
                                            self.parameter['channel'])
            # Else if that channel is found inside the file
            elif self._check_for_channel(data_file, self.parameter['channel']):
                grid_options = grid_options + " -cn {} -cn_fix {}"\
                                    .format(self.parameter['channel'],
                                            self.parameter['channel'])
        # Make the grid with chosen options
        status = self.make_grid(data_file, grid_path, grid_options)
        # Return status code 0 if all ran well
        return status


    def make_grid(self, data_file, grid_file, grid_options=""):
        # Command:
        # minrng - exclude data below minimum range
        # vemax - exclude data above max velocity
        # xtd - extended output including power and spectral width and errors
        make_grid_command = "make_grid {gridoptions} -xtd"\
                            " -minrng 10"\
                            " -vemax {max_velocity}"\
                            " {datafile} > {gridpath}"\
                            "".format(gridoptions=grid_options,
                                      max_velocity=RstConst.VEMAX,
                                      datafile=data_file,
                                      gridpath=grid_file)

        try:
            logging.info('*** MAKE GRID ***')
            check_rst_command(make_grid_command, grid_file)
            return 0

        except RSTException as err:
            logging.warn(err)
            self.radars_errors += data_file + '\n'
            return 1

        except RSTFileEmptyException as err:
            self.radars_errors += data_file + '\n'
            logging.warn(err)
            os.remove(grid_file)
            return 1


    def generate_grid_files(self):
        """
        Generates the grid files used in the map generation step.
        """
        radar_abbrv = []
        if self.parameter['hemisphere'] == 'south':
            radar_abbrv = SouthRadar.RADAR_ABBRV
        else:
            radar_abbrv = NorthRadar.RADAR_ABBRV

        grid_file_counter = 0
        ext = 'fitacf'
        for abbrv in radar_abbrv:
            file_pattern = "{data_path}/{date}*{abbrv}*.{ext}.bz2"\
                    "".format(data_path=self.parameter['data_path'],
                              date=self.parameter['date'],
                              abbrv=abbrv,
                              ext=ext)
            for data_file in glob(file_pattern):
                try:
                    # More Sanity checks, because the method is public
                    # we have to make sure the user is providing correct file types
                    data_file_ext = data_file.split('.')[-1]
                    if data_file_ext not in FileConst.COMPRESSION_TYPES and \
                       data_file_ext not in FileConst.FILE_TYPE:
                        msg = "Error: {datafiletype} file type or compression extension"\
                                " is not supported. Please use one for the following"\
                                " supported types: {filetypes} {compressiontypes}"\
                                "".format(datafiletype=data_file_ext,
                                          filetypes=FileConst.FILE_TYPE,
                                          compressiontypes=FileConst.COMPRESSION_TYPES)
                        logging.error(msg)
                        raise UnsupportedTypeException(msg)
                    if not os.path.isfile(data_file):
                        raise FileDoesNotExistException(data_file)

                    # if the data file is not in data path then check in the
                    # in the current directory.
                    data_path = "{path}/{filename}"\
                                "".format(path=self.parameter['plot_path'],
                                          filename=os.path.basename(data_file))

                    try:
                        shutil.copy2(data_file, self.parameter['plot_path'])
                        data_file = "{path}/{filename}"\
                                "".format(path=self.parameter['plot_path'],
                                          filename=os.path.basename(data_file))
                    except shutil.Error as msg:
                        logging.warn(msg)
                        logging.warn("{datafile} was not found in the data_path:"
                                     " {data_path} or plot_path: {plot_path},"
                                     " this file will not be used"
                                     "in the convection map process"
                                     "".format(data_path=self.parameter['data_path'],
                                               datafile=data_file,
                                               plot_path=self.parameter['plot_path']))
                        self.radars_missing += data_file + '\n'
                        message = "File {datafile} was not found, please make sure to"\
                                  " provide data path using -d option and that the"\
                                  " file exist in the folder".format(datafile=data_file)
                        raise OSError(message)  # TODO: better exception?
                    
                    if data_file_ext in FileConst.COMPRESSION_TYPES:
                        try:
                            compression_command = "{command} {datapath}"\
                                                  "".format(command=FileConst.EXT[data_file_ext],
                                                            datapath=data_path)
                            sp.call(compression_command, shell=True)
                            data_file = re.sub('.'+data_file_ext, '', data_file)
                        except KeyError as err:
                            logging.warn(err)
                            msg = "Error: The compression extension {compressionext} "\
                                  "does not have a corresponding compression command"\
                                  " associated. Please use one of the following"\
                                  " implmented compressions types {compression}"\
                                  "".format(compressionext=data_file_ext,
                                            compression=FileConst.EXT)
                            raise KeyError(msg)
                    file_name = os.path.basename(data_file)
                    logging.info('Reading in data from: {}'.format(str(file_name)))
                    self.radars_used += '{} \n'.format(str(file_name))
                    if os.path.getsize(data_file) == 0:
                        logging.warn(EmptyDataFileWarning(data_file))
                        self.radars_errors += data_file + '\n'
                        raise RSTFileEmptyException(data_file)
                except Exception as err:
                    logging.error(err)
                    continue

            try:
                filename = "{path}/{date}*{abbrv}*.{ext}"\
                           "".format(path=self.parameter['plot_path'],
                                     date=self.parameter['date'],
                                     abbrv=abbrv,
                                     ext=ext)
                # If files exist for this radar
                if glob(filename):
                    result = self.generate_radar_grid_file(abbrv, filename)
                    if result == 0: 
                        grid_file_counter+=1
            except Exception as err:
                print(err)
                logging.error(err)
                continue

        # useful logging information for the user
        logging.info(self.radars_used)
        logging.info(self.radars_errors)

        if grid_file_counter == 0:
            logging.error(NoGridFilesException)
            raise NoGridFilesException(radar_abbrv)

        grd_filename = "{date}.{hemisphere}.grd".format(date=self.parameter['date'],
                                                        hemisphere=self.hem_ext)
        grd_path = "{plot_path}/{grd_file}"\
                   "".format(plot_path=self.parameter['plot_path'],
                             grd_file=grd_filename)

        combine_grid_command = "combine_grid {options} {plot_path}/{date}."\
                               "*.{hemisphere}.grid  > {grdpath}"\
                               "".format(options=self.rst_options,
                                         plot_path=self.parameter['plot_path'],
                                         date=self.parameter['date'],
                                         grdpath=grd_path,
                                         hemisphere=self.hem_ext)

        logging.info('*** COMBINE GRID ***')
        check_rst_command(combine_grid_command, grd_path)


    def generate_map_files(self):
        """
        Generates map files for the radar fitacf files availible for
        the given date and hemisphere. Clean up any leftover files using
        ConvectionMap.cleanup()
        """
        # Make Empty Map File
        map_grd_options = ""

        if self.parameter['hemisphere'] == "south":
            map_grd_options = self.rst_options + " -sh"

        grd_path = "{plot_path}/{date}.{hemisphere}.grd"\
                   "".format(plot_path=self.parameter['plot_path'],
                             date=self.parameter['date'],
                             hemisphere=self.hem_ext)
        file_exists(grd_path)
        empty_map_filename = "{date}.{hemisphere}.empty.map"\
                             "".format(date=self.parameter['date'],
                                       hemisphere=self.hem_ext)
        empty_map_path = "{plot_path}/{empty_map}"\
                         "".format(plot_path=self.parameter['plot_path'],
                                   empty_map=empty_map_filename)

        map_grd_command = "map_grd {options} -l 50 "\
                          "{plot_path}/{date}.{hemisphere}.grd > "\
                          "{plot_path}/{filename}"\
                          "".format(options=map_grd_options,
                                    plot_path=self.parameter['plot_path'],
                                    date=self.parameter['date'],
                                    filename=empty_map_filename,
                                    hemisphere=self.hem_ext)

        logging.info('*** MAKE EMPTY MAP ***')
        check_rst_command(map_grd_command, empty_map_path)

        # Make HMB file
        hmb_map_filename = "{date}.{hemisphere}.hmb.map"\
                "".format(date=self.parameter['date'],
                          hemisphere=self.hem_ext)
        hmb_map_path = "{plot_path}/{hmb_map}"\
                       "".format(plot_path=self.parameter['plot_path'],
                                 hmb_map=hmb_map_filename)

        map_addhmb_command = "map_addhmb {options} {plot_path}/{empty_map} >"\
                             " {plot_path}/{hmb_map}"\
                             "".format(options=self.rst_options,
                                       plot_path=self.parameter['plot_path'],
                                       empty_map=empty_map_filename,
                                       hmb_map=hmb_map_filename)

        logging.info('*** ADD HMB ***')
        check_rst_command(map_addhmb_command, hmb_map_path)

        # Make imf file
        imf_filename = '{imf_path}/{date}_imf.txt'.format(imf_path=self.parameter['imf_path'],
                                                          date=self.parameter['date'])
        imf_map_filename = "{date}.{hemisphere}.imf.map"\
                           "".format(date=self.parameter['date'],
                                     hemisphere=self.hem_ext)
        imf_map_path = "{map_path}/{imf_map}"\
                       "".format(map_path=self.parameter['map_path'],
                                 imf_map=imf_map_filename)

        # If there are no pre-existing files
        if not os.path.exists(imf_filename):
            omni = Omni(self.parameter['date'], self.parameter['map_path'])

            try:
                # Make sure the files you have are updated
                update = omni.check_for_updates()
                if update:
                    old_omni_file = "{map_path}/{date}_omni_{currentdate}.txt"\
                                    "".format(map_path=self.parameter['map_path'],
                                              date=self.parameter['date'],
                                              currentdate=self._current_date.strftime("%Y%m%d"))
                    try:
                        shutil.move(omni.omni_path, old_omni_file)
                    except IOError as err:
                        logging.exception(err)
                        pass
            except OmniFileNotFoundWarning as warning_msg:
                logging.warn(warning_msg)
                update = True

            # If there are no existing files, go get them from omni
            try:
                if update:
                    omni.get_omni_file()
                # Convert the omni output to imf RST format
                omni.omnifile_to_IMFfile()

                imf_filename = '{map_path}/{imf_file}'.format(map_path=self.parameter['map_path'],
                                                              imf_file=omni.imf_filename)


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

        map_addimf_command = "map_addimf {options} -omni -d 00:10"\
                             " -if {imf_file}"\
                             " {plot_path}/{hmb_map} >"\
                             " {plot_path}/{imf_map}"\
                             "".format(options=self.rst_options,
                                       plot_path=self.parameter['plot_path'],
                                       imf_file=imf_filename,
                                       hmb_map=hmb_map_filename,
                                       imf_map=imf_map_filename)

        logging.info('*** ADD IMF ***')
        check_rst_command(map_addimf_command, imf_map_path)
        self._imf_option = " -imf"
        input_model_file = imf_map_filename

        # Make model map file
        map_model_filename = "{date}.{hemisphere}.model.map"\
                             "".format(date=self.parameter['date'],
                                       hemisphere=self.hem_ext)
        map_model_path = "{plot_path}/{map_model}"\
                         "".format(plot_path=self.parameter['plot_path'],
                                   map_model=map_model_filename)

        map_addmodel_command = "map_addmodel {options} -o 6 -d l "\
                               "{plot_path}/{input_map} > {plot_path}/{model_map}"\
                               "".format(options=self.rst_options,
                                         plot_path=self.parameter['plot_path'],
                                         input_map=input_model_file,
                                         model_map=map_model_filename)
        logging.info('*** ADD MODEL ***')
        check_rst_command(map_addmodel_command, map_model_path)

        # Final map fit files
        if self.parameter['hemisphere'] == 'south':
            map_filename = "{date}.s.map".format(date=self.parameter['date'])
        elif self.parameter['hemisphere'] == 'north':
            map_filename = "{date}.n.map".format(date=self.parameter['date'])
        else:
            map_filename = "{date}.canadian.map".format(date=self.parameter['date'])

        map_path = "{plot_path}/{map_file}"\
                   "".format(plot_path=self.parameter['plot_path'],
                             map_file=map_filename)

        map_fit_command = "map_fit {options} {plot_path}/{model_map} >"\
                          " {plot_path}/{map_file}"\
                          "".format(options=self.rst_options,
                                    plot_path=self.parameter['plot_path'],
                                    model_map=map_model_filename,
                                    map_file=map_filename)
        logging.info('*** MAP FITTING ***')
        check_rst_command(map_fit_command, map_path)
        try:
            shutil.copy2(map_path, self.parameter["map_path"] +
                         "/{date}.map".format(date=self.parameter['date']))
        except shutil.Error:
            pass


    def generate_RST_convection_maps(self):
        """
        Generates the convection maps using the RST map_plot function.
        """

        logging.info("Generating Convection Maps using RST ")
        # TODO: A better method of importing the key file and
        # what to do when it is not provided
        key_option = "-vkeyp -vkey rainbow.key"
        map_path = "{map_path}/{date}.map"\
                   "".format(map_path=self.parameter['map_path'],
                             date=self.parameter['date'])

        post_script_path = "{}/*.ps".format(self.parameter['plot_path'])
        file_exists(map_path)
        map_plot_command = "map_plot {options} -ps -mag"\
                           " -st {start_time} -et {end_time} -rotate -hmb -modn"\
                           " -fit -grd -ctr {imf} -dn -extra -coast -vecp "\
                           " -pot -time {key} -path {plot_path} {map_path}"\
                           " 2>/dev/null"\
                           "".format(options=self.rst_options,
                                     start_time=self.parameter['start_time'],
                                     end_time=self.parameter['end_time'],
                                     imf=self._imf_option,
                                     key=key_option,
                                     plot_path=self.parameter['plot_path'],
                                     map_path=map_path)
        logging.info(map_plot_command)
        check_rst_command(map_plot_command, post_script_path)

        for ps_file in glob(post_script_path):
            image_filename = ps_file.replace(".ps", "")
            convert_command = "convert -density 200 {ps_filename} "\
                              " {plot_path}/{filename}.{ext}"\
                              "".format(plot_path=self.parameter['plot_path'],
                                        ps_filename=ps_file,
                                        filename=image_filename,
                                        ext=self.parameter['image_ext'])
            return_value = sp.call(convert_command.split())
            if return_value != 0:
                logging.warn(ConvertWarning(ps_file,
                                            self.parameter['image_ext']))

    def cleanup(self):
        """
        Cleans up any meta or data that should not be stored in the plot path.
        """
        path = "{plot_path}/{date}".format(plot_path=self.parameter['plot_path'],
                                           date=self.parameter['date'])

        try:
            shutil.copy2(self.parameter['logfile'], self.parameter['map_path'])
        except Exception:
            pass

        for f in glob(path+'*.fitacf'):
            os.remove(f)
        for f in glob(path+'*.grid'):
            os.remove(f)
        for f in glob(path+'*.map'):
            os.remove(f)
        for ext in FileConst.FILE_TYPE:
            for f in glob('{path}*.{ext}*'.format(path=path, ext=ext)):
                os.remove(f)

        for f in glob(path + "*.grd"):
            os.remove(f)


if __name__ == '__main__':
    import sys
    convec = ConvectionMaps(sys.argv[1:])
    convec.generate_grid_files()
    convec.generate_map_files()
    # convec.generate_RST_convection_maps()
    # convec.cleanup()
