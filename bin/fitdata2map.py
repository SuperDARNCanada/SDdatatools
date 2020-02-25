#!/usr/bin/env python

# Copyright 2017 SuperDARN Canada
#
# Marina Schmidt
#
# fitacf2convectionMap.py
# 2018-01-26

import sys
from DARNprocessing import ConvectionMaps

convec_map = ConvectionMaps(sys.argv[1:])
convec_map.generate_grid_files()
convec_map.generate_map_files()
convec_map.cleanup()
exit(0)
