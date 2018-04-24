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

class Fitacf2ConvectionMap(ConvectionMaps):
    """
    Converts various radar fitacf data and user input options to convection maps.

    """
        def __init__(self,arguments):
            ConvectionMaps.__init__(self, arguments)


        def



if __name__ == '__main__':
    Fitacf2ConvectionMap(sys.argv[1:])
