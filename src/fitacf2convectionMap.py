#!/usr/bin/env python

# Copyright 2017 SuperDARN Canada
#
# Marina Schmidt
#
# fitacf2convectionMap.py
# 2018-01-26

import os
import time
import sys
import argparse

class Fitacf2ConvectionMap():
    """
    Converts various radar fitacf data and user input options to convection maps.

    """

    def __init__(self,arguements):
        """
        Reads in user command line options and parses them to correct member
        fields.

        usage: fitacf2convectionmap [-h] [--hemisphere {north,south,both}]
                                    [--start-time hh:mm] [--end-time hh:mm]
                                    [--rst-version N] [-i EXTENSION] [-f PATH]
                                    [-p PATH] [-o PATH] [-n NUMPROCESSORS] [-v]
                                    date

        Converts fitacf files to convection maps

        positional arguments:
          date                  The date of the fitacf data. Format: YYYYMMDD

        optional arguments:
          -h, --help            show this help message and exit
          --hemisphere {north,south,both}
                                The hemisphere you want to assimilate. Default: both
          --start-time hh:mm    The start time at hh:mm of the fitacf data. Default:
                                00:00
          --end-time hh:mm      The end time at hh:mm of the fitacf data. Default:
                                23:59
          --rst-version N       The version number of RST that you are using. Default:
                                4.1
          -i EXTENSION, --image-extension EXTENSION
                                The image format of convection maps. Default: pdf
          -f PATH, --fitacfpath PATH
                                The absolute path to the fitacf data. Default:
                                /home/marina/superDARN/mapping/mapping/src
          -p PATH, --plotpath PATH
                                The absolute path to where the convection maps will be
                                saved. Default:
                                /home/marina/superDARN/mapping/mapping/src
          -o PATH, --omnipath PATH
                                The absolute path to where the omni files will be
                                saved to. Default:
                                /home/marina/superDARN/mapping/mapping/src
          -n NUMPROCESSORS      The number of processors you wish to use in parallel
                                mode. This option enables parallel mode. Default: 1
          -v, --verbose         Turns on verbose mode.

        """

        self.current_path = os.getcwd()

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
        parser.add_argument('--hemisphere',type=str,
                            choices=['north','south','both'],default='both',
                            help='The hemisphere you want to assimilate.'
                            ' Default: both')
        parser.add_argument('--start-time',type=str,
                            metavar='hh:mm',default='00:00',
                            help='The start time at hh:mm of the fitacf data.'
                            ' Default: 00:00')
        parser.add_argument('--end-time',type=str,
                            metavar='hh:mm',default='23:59',
                            help='The end time at hh:mm of the fitacf data.'
                            ' Default: 23:59')
        parser.add_argument('--rst-version',type=str,
                            metavar='N',default='4.1',
                            help='The version number of RST that'
                            ' you are using. Default: 4.1')
        parser.add_argument('-i','--image-extension',type=str,
                            metavar='EXTENSION',default='pdf',
                            help='The image format of convection maps.'
                            ' Default: pdf')

        # Path options
        parser.add_argument('-f','--fitacfpath',type=str,
                             metavar='PATH',default=self.current_path,
                             help='The absolute path to the fitacf data.'
                            ' Default: {}'.format(self.current_path))
        parser.add_argument('-p','--plotpath',type=str,
                            metavar='PATH',default=self.current_path,
                            help='The absolute path to where the convection'
                            ' maps will be saved. Default: {}'.format(self.current_path))
        parser.add_argument('-o','--omnipath',type=str,
                            metavar='PATH',default=self.current_path,
                            help='The absolute path to where the omni files'
                            ' will be saved to. Default: {}'.format(self.current_path))
        # Parallel options
        parser.add_argument('-n',type=int,
                            metavar='NUMPROCESSORS',default=1,
                            help='The number of processors you wish to use'
                            ' in parallel mode. '
                            ' This option enables parallel mode.'
                            ' Default: 1')

        # Standard options, note: the help option is handled by argparse
        parser.add_argument('-v','--verbose',action='store_true',
                            help='Turns on verbose mode.')


        self.parameter = parser.parse_args()

        def _usage_message():
            print("Try 'fitacf2convectionmap' for more information.")


if __name__ == '__main__':
    Fitacf2ConvectionMap(sys.argv[1:])
