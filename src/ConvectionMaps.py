#!/usr/bin/env python

# Copyright 2017 SuperDARN Canada
#
# Marina Schmidt
#
# fitacf2convectionMap.py
# 2018-01-26

from __future__ import print_function

from datetime import datetime
from distutils.ccompiler import mkpath
from subprocess import call, check_output, CalledProcessError
from glob import glob
from utils import check_rst_command
from convectionMapConstants import ErrorCodes, NorthRadar, SouthRadar, RstConst
from convectionMapExceptions import (RSTException, RSTFileEmptyException,
                                     NoGridFilesException)
from convectionMapWarnings import (ConvertWarning, OmniFileNotFoundWarning,
                                   EmptyDataFileWarning, FileNotFoundWarning)
from warnings import warn
from omni import Omni

import logging
import shutil
import os
import argparse
import re


class ConvectionMaps():

    def __init__(self, arguements):
        """
        Reads in user command line options and parses them to correct member
        fields.
        """

        self._current_date = datetime.now()
        self._current_path = os.getcwd()


        #
        # TODO: place this in utils module if other scripts have similar options
        #

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

        parser.add_argument('--hemisphere', type=str,
                            choices=['north', 'south'], default='north',
                            help='The hemisphere you want to assimilate.'
                            ' Default: north')
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
        # formats and in the future is might be easier for the user to
        # to inherit this class and then modify as needed for the format.
        # TODO: decide whether this should be taken out.
        # parser.add_argument('-f','--data-format',type=str,
        #                    choices=['fitacf','fit','fitred'],default='fitacf ',
        #                    help='The data format to use for generating the'
        #                    ' convection maps Default: fitacf')

        # Path options
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
        parser.add_argument('-k','--keypath',type=str,
                            metavar='PATH',default=self._current_path,
                            help="The absolute path to the key file for"\
                            "the convection maps."\
                            " Default: {}".format(self._current_path))

        # Parallel options
        parser.add_argument('-n', type=int,
                            metavar='NUMPROCESSORS', default=1,
                            help='The number of processors you wish to use'
                            ' in parallel mode. '
                            ' This option enables parallel mode.'
                            ' Default: 1')

        # Standard options, note: the help option is handled by argparse
        parser.add_argument('-v', '--verbose', action='store_true',
                            help='Turns on verbose mode.')

        self.parameter = parser.parse_args()
        self.channel = ['', 'a', 'b', 'c', 'd']

        self.parameter = vars(self.parameter)

        if self.parameter['rst_version'] < 4.1:
            self.rst_options = "-new "
        else:
            self.rst_options = ""

        log_filename = self.parameter['date'] + '_ConvectionMap_logfile.log'
        FORMAT = "%(levelname)s %(asctime)-15s: %(message)s"
        logging.basicConfig(filename=log_filename,
                            format=FORMAT,
                            level=logging.DEBUG)
        logging.info('Parameter list:'+ str(self.parameter))
        self.radars_used = 'Radar files uses in the Convection Map process:\n'
        self.radars_missing = 'Radar files missing'\
                ' (not used in the Convection Map process):\n'
        self.radars_errors = 'Radars files that raised errors:\n'

    def setup_paths(self):
        """
        setup the folder organization for archiving data
        """
        # current date folder? Do we want this for secondary storage?
        folder_organization = "/{date}/{hemisphere}/"\
                "{currentdate}"\
                "".format(date=self.parameter['date'],
                          hemisphere=self.parameter['hemisphere'],
                          currentdate=self._current_date.strftime("%Y%m%d"))

        if self.parameter['omnipath'] == self.parameter['plotpath']:
            self.parameter['omnipath'] += folder_organization

        if self.parameter['mappath'] == self.parameter['plotpath']:
            self.parameter['mappath'] += folder_organization

        self.parameter['plotpath'] += folder_organization

        # creates the paths if they are not already created.
        mkpath(self.parameter['plotpath'])
        mkpath(self.parameter['mappath'])
        mkpath(self.parameter['omnipath'])

        logging.info('The following data files will be'
                     ' stored in the following paths')
        logging.info('Plot path: ' + self.parameter['plotpath'])
        logging.info('Map files path' + self.parameter['mappath'])
        logging.info('Omni file path": ' + self.parameter['omnipath'])
        logging.info('The data for the convections maps is obtained from')
        logging.info('Data path: ' + self.parameter['datapath'])


    # TODO: implement parallel version
    def _generate_radar_grid_file(self,radar_abbrv, radar_ext):

        data_date = datetime.strptime(self.parameter['date'], "%Y%m%d")
        data_year = data_date.strftime("%Y")
        data_month = data_date.strftime("%m")

        data_filename = "{date}.{ext}".format(date=self.parameter['date'],
                                               ext=radar_ext)

        grid_filename = "{date}.{abbrv}.*.grid".format(date=self.parameter['date'],
                                                     abbrv=radar_abbrv)

        data_path = "{datapath}/{data_file}"\
                "".format(datapath=self.parameter['plotpath'],
                          data_file=data_filename)
        grid_path = "{datapath}/{grid_file}"\
                "".format(datapath=self.parameter['plotpath'],
                          grid_file=grid_filename)

        # if the data file is not in the current file then check in the
        # in the provided data folder.
        if not os.path.isfile(data_path):
            data_path = "{datapath}/{datafile}.gz"\
                    "".format(datapath=self.parameter['datapath'],
                              datafile=data_filename)
            print(data_path)
            try:
                shutil.copy2(data_path, self.parameter['plotpath'])
                data_path = "{datapath}/{data_file}"\
                        "".format(datapath=self.parameter['plotpath'],
                                  data_file=data_filename)

            except IOError as e:
                logging.warn(e)
                self.radars_missing += data_filename + '\n'
                return ErrorCodes.ERRFILENOTFOUND

            gzip_command = "gzip -d {}.gz".format(data_path)

            if call(gzip_command.split()) != 0:
                logging.warn(FileNotFoundWarning(data_filename))
                self.radars_errors += data_filename + '\n'
                return ErrorCodes.ERRFILENOTFOUND

        elif os.path.isfile(grid_path):
            self.radars_used += data_filename + '\n'
            return 0

        if os.path.getsize(data_path) == 0:
            logging.warn(EmptyDataFileWarning(data_filename))
            self.radars_errors += data_filename + '\n'
            return ErrorCodes.ERREMPTYFILE

        if 'C.fit' in data_filename:
            try:
                data_filename, radar_abbrv = self.convert_fit_to_fitacf(data_path)
            except RSTException as err:
                logging.exception(err)
                return ErrCodes.ERRRST

            data_path = "{datapath}/{data_file}"\
                    "".format(datapath=self.parameter['plotpath'],
                              data_file=data_filename)

        dmapdump_command = "dmapdump {} | grep -c '\"scan\" = -1'"\
                "".format(data_path)


        grid_options = self.rst_options

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
            grid_options = self.rst_options + "-tl 60 "

        channelA = self._check_for_channel(data_filename, 1)
        channelB = self._check_for_channel(data_filename, 2)
        monochannel = self._check_for_channel(data_filename, 0)


        if '.a.' in data_filename:
            grid_options = grid_options + " -cn_fix a"
        elif '.b.' in data_filename:
            grid_options = grid_options + " -cn_fix a"
        elif '.c.' in data_filename:
            grid_options = grid_options + " -cn_fix c"
        elif '.d.' in data_filename:
            grid_options = grid_options + " -cn_fix d"
        elif self.parameter['channel'] == 0:
                grid_filename = "{date}.{abbrv}."\
                                "grid".format(date=self.parameter["date"],
                                              abbrv=radar_abbrv)
        elif self.parameter['channel'] == 1:
                grid_filename = "{date}.{abbrv}.a."\
                                "grid".format(date=self.parameter["date"],
                                              abbrv=radar_abbrv)
                grid_options = grid_options + " -cn A"
        elif self.parameter['channel'] == 2:
                grid_filename = "{date}.{abbrv}.b."\
                                "grid".format(date=self.parameter["date"],
                                              abbrv=radar_abbrv)
                grid_options = grid_options + " -cn B"
        else:
            if monochannel > 0:
                grid_filename = "{date}.{abbrv}."\
                                "grid".format(date=self.parameter["date"],
                                          abbrv=radar_abbrv)
                self.make_grid(data_filename, grid_filename, grid_options)

            if channelA > 0:
                grid_filename = "{date}.{abbrv}.a."\
                                "grid".format(date=self.parameter["date"],
                                          abbrv=radar_abbrv)
                grid_optionsA = grid_options + " -cn A"
                self.make_grid(data_filename, grid_filename, grid_optionsA)

            if channelB > 0:
                grid_filename = "{date}.{abbrv}.b."\
                                "grid".format(date=self.parameter["date"],
                                             abbrv=radar_abbrv)
                grid_optionsB = grid_options + " -cn B"
                self.make_grid(data_filename, grid_filename, grid_optionsB)
            return 0

        self.make_grid(data_filename, grid_filename, grid_options)
        return 0

    # Maybe move this function to utils?
    def _check_for_channel(self, data_filename, channel_num):
        """
        A method to check for the channel number in a fitacf file
        that may use mono and stero.
        """
        channel_command = "dmapdump {plotpath}/{filename} "\
                "| grep -c '\"channel\" = {channel}'"\
                "".format(plotpath=self.parameter['plotpath'],
                          filename=data_filename,
                          channel=channel_num)
        try:
            channel_count = check_output(channel_command, shell=True)
        except CalledProcessError as e:
            channel_count = e.output  # Gets the output of the command
        return int(channel_count)


    def make_grid(self, data_filename, grid_filename, grid_options=""):
        make_grid_command = "make_grid {gridoptions} -xtd"\
                " -i {integration_time} -minrng {minrange}"\
                " -vemax {max_velocity}"\
                " {plotpath}/{datafile} > {plotpath}/{filename}"\
                "".format(gridoptions=grid_options,
                          integration_time=RstConst.INTEGRATION_TIME,
                          minrange=RstConst.MIN_RANGE,
                          max_velocity=RstConst.VEMAX,
                          plotpath=self.parameter['plotpath'],
                          datafile=data_filename,
                          filename=grid_filename)

        grid_path = "{plotpath}/{filename}"\
                "".format(plotpath=self.parameter['plotpath'],
                          filename=grid_filename)
        logging.info(make_grid_command)
        try:
            check_rst_command(make_grid_command, grid_path)
        except RSTException as err:
            logging.warn(err)
            self.radars_errors += data_filename + '\n'
        except RSTFileEmptyException as err:
            self.radars_errors += data_filename + '\n'
            logging.warn(err)
            os.remove(grid_filename)

    # TODO: might be a util method
    def convert_fit_to_fitacf(self, filename):
        """
        Converts fit data to fitacf with the standard naming convention used for
        superDARN data.
        Retruns the fitacf filename that the fit data was saved to and the radar
        abbrevation associated to the letter.
        """
        match = re.search(r'([a-z])', filename)
        radar_letter = match.group()
        if self.parameter['hemisphere'] == 'south':
            radar_abbrv = SouthRadar.SINGLE_TO_ABBRV[radar_letter]
        else:
            radar_abbrv = NorthRadar.SINGLE_TO_ABBRV[radar_letter]

        fitacf_path = "{plotpath}/{date}.C0.{abbrv}."\
                          "fitacf".format(date=self.parameter['date'],
                                          abbrv=radar_abbrv)
        fittofitacf_command = "fittofitacf {plotpath}/{filename} >"\
                              " {fitacf_filename}"\
                              "".format(filename=filename,
                                        plotpath=self.parameter['plotpath'],
                                        fitacf_filename=fitacf_path)
        check_rst_command(fittofitacf_command,fitacf_path)

        return (fitacf_filename, radar_abbrv)

    def generate_grid_files(self):
        radar_list = {}
        if self.parameter['hemisphere'] == 'south':
            if self.parameter['channel'] == 0:
                radar_list.update( SouthRadar.SINGLE_EXTENSIONS)
                radar_list.update( SouthRadar.ABBRV_EXTENSIONS)
            elif self.parameter['channel'] == 1:
                radar_list.update(SouthRadar.SINGLE_EXTENSIONS)
                radar_list.update(SouthRadar.ABBRV_EXTENSIONS)
                radar_list.update(SouthRadar.CHANNEL_ONE_EXTENSIONS)
            elif self.parameter['channel'] == 1:
                radar.update(SouthRadar.SINGLE_EXTENSIONS)
                radar.update(SouthRadar.ABBRV_EXTENSIONS)
                radar.update(SouthRadar.CHANNEL_TWO_EXTENSIONS)
            elif self.parameter['channel'] == 3:
                radar_list.update(SouthRadar.CHANNEL_THREE_EXTENSIONS)
            elif self.patamter['channel'] == 4:
                radar_list.update(SouthRadar.CHANNEL_FOUR_EXTENSIONS)
            else:
                radar_list.update(SouthRadar.SINGLE_EXTENSIONS)
                radar_list.update(SouthRadar.ABBRV_EXTENSIONS)
                radar_list.update(SouthRadar.CHANNEL_ONE_EXTENSIONS)
                radar_list.update(SouthRadar.CHANNEL_TWO_EXTENSIONS)
                radar_list.update(SouthRadar.CHANNEL_THREE_EXTENSIONS)
                radar_list.update(SouthRadar.CHANNEL_FOUR_EXTENSIONS)
        else:
            if self.parameter['channel'] == 0:
                radar_list.update(NorthRadar.SINGLE_EXTENSIONS)
                radar_list.update(NorthRadar.ABBRV_EXTENSIONS)
            elif self.parameter['channel'] == 1:
                radar_list.update(NorthRadar.SINGLE_EXTENSIONS)
                radar_list.update(NorthRadar.ABBRV_EXTENSIONS)
                radar_list.update(NorthRadar.CHANNEL_ONE_EXTENSIONS)
            elif self.parameter['channel'] == 1:
                radar_list.update(NorthRadar.SINGLE_EXTENSIONS)
                NorthRadar.update(ABBRV_EXTENSIONS)
                NorthRadar.update(CHANNEL_TWO_EXTENSIONS)
            elif self.parameter['channel'] == 3:
                radar_list.update(NorthRadar.CHANNEL_THREE_EXTENSIONS)
            elif self.parameter['channel'] == 4:
                radar_list.update(NorthRadar.CHANNEL_FOUR_EXTENSIONS)
            else:
                radar_list.update(NorthRadar.SINGLE_EXTENSIONS)
                radar_list.update(NorthRadar.ABBRV_EXTENSIONS)
                radar_list.update(NorthRadar.CHANNEL_ONE_EXTENSIONS)
                radar_list.update(NorthRadar.CHANNEL_TWO_EXTENSIONS)
                radar_list.update(NorthRadar.CHANNEL_THREE_EXTENSIONS)
                radar_list.update(NorthRadar.CHANNEL_FOUR_EXTENSIONS)

        grid_file_counter = 0
        for radar_abbrv,ext in radar_list.iteritems():
            if ext == 'fit':
                radar_ext = radar_abbrv + '.C.' + ext
            else:
                radar_ext = 'C0.' + radar_abbrv + '.' + ext

            if self._generate_radar_grid_file(radar_abbrv,radar_ext) != 0:
                grid_file_counter += 1

        logging.info(self.radars_used)
        logging.info(self.radars_missing)
        logging.info(self.radars_errors)

        if grid_file_counter == len(radar_list):
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

        empty_map_filename = "{date}.empty.map".format(date=self.parameter['date'])
        empty_map_path = "{plotpath}/{empty_map}"\
                "".format(plotpath=self.parameter['plotpath'],
                          empty_map=empty_map_filename)

        map_grd_command = "map_grd {options} -l 50 {plotpath}/{date}.grd > "\
                "{plotpath}/{filename}"\
                "".format(options=map_grd_options,
                          plotpath=self.parameter['plotpath'],
                          date=self.parameter['date'],
                          filename=empty_map_filename)

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

        return_value = 0
        try:
            if omni.check_for_updates():
                old_omni_file = "{omnipath}/{date}_omni_{currentdate}.txt"\
                       "".format(date=self.parameter['date'],
                                 currentdate=self._current_date.strftime("%Y%m%d"))
                try:
                    shutil.move(omni.omni_path,old_omni_file)
                except IOError as err:
                    logging.exception(err)
                    pass
                return_value = omni.get_omni_file()
        except OmniFileNotFoundWarning:
            return_value = omni.get_omni_file()

        if omni.omnifile_to_IMFfile() == 0 and return_value == 0:
            imf_map_filename = "{date}.imf.map"
            imf_map_path = "{omnipath}/{imf_map}"\
                    "".format(plotpath=self.parameter['omnipath'],
                              imf_map=imf_map_filename)

            map_addimf_command = "map_addimf {options} -d 00:10"\
                    " -if {omnipath}/{imf_filename} {plotpath}/{hmb_map} >"\
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
        else:
            self._imf_option = ""
            input_model_file = hmb_map_filename

        map_model_filename = "{date}.model.map"
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

        loggin.info("Generating Convection Maps uring RST ")
        # TODO: A better method of importing the key file and
        # what to do when it is not provided
        shutil.copy2("{keypath}/rainbow.key".format(self.parameter['keypath']), ".")
        key_option = "-vkey -vkey rainbow.key"
        map_path = "{mappath}\{date}.map"\
                "".format(mappath=self.parameter['mappath'],
                          date=self.parameter['date'])

        post_script = "{}/*.ps".format(self.parameter['plotpath'])
        utils.file_exists(map_path)
        map_plot_command = "map_plot {options} -ps -mag"\
                " -st {start_time} -et {end_time} -rotate -hmb -modn"\
                " -fit -grd -ctr {imf} -dn -extra -cost -vecp "\
                " -pot -time {key} {mappath}"\
                " 2>/dev/null"\
                "".format(options=self.rst_options,
                          start_time=self.parameter['start-time'],
                          end_time=self.parameter['end-time'],
                          imf=self._imf_option,
                          key=key_option,
                          mappath=map_path)

        logging.info(map_plot_command)
        check_rst_command(map_plot_command, "*.ps")

        for ps_file in glob("*.ps"):
            image_filename = ps_file.replace(".ps", "")
            convert_command = "convert -density 200 {plotpath}ps_filename}"\
                    " {plotpath}/{filename}.{ext}"\
                    "".format(plotpath=self.parameter['plotpath'],
                              ps_filename=ps_file,
                              filename=image_filename,
                              ext=self.parameter['image-extension'])
            return_value = call(convert_command.split())
            if return_value != 0:
                logging.warn(ConvertWarning(ps_file,
                                            self.parameter['image-extension']))

    def cleanup(self):

        os.remove(self.parameter['plotpath'] + "/*.grid")
        os.remove(self.parameter['plotpath'] + "/*.grd")
        os.remove(self.parameter['plotpath'] + "/*.*.map")
        os.remove(self.parameter['plotpath'] + "/*.fitacf")
        os.remove(self.parameter['plotpath'] + "/*.fit")


if __name__ == '__main__':
    import sys
    convec = ConvectionMaps(sys.argv[1:])
    convec.setup_paths()
    convec.generate_map_files()

