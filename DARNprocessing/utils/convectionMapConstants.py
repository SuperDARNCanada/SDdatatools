#!/usr/bin/python

# Copyright 2017 SuperDARN Canada
#
# Marina Schmidt
#
# constants.py
# 2018-01-31
# Create classes containing constants that the script will need.


# The constants are defined at class-level and not module-level.
# I know this is not PEP8 style however, it is a prefferred
# method to keep seperation, readibility, and if the coder wants to
# create errors on attempts to change the constants they can do it in the class.
class RstConst():
    INTEGRATION_TIME = 120
    MIN_RANGE = 2
    VEMAX = 1000000


class OmniConst():
    DELAY = 600

"""
 Southern Hemisphere Radar Extensions:
 Halley (hal) (h)
 Syowa South (sys) (j)
 Sanae (san) (d)
 Syowa East (sye) (n)
 Kerguelen (ker) (p)
 TIGER Tasmania (tig) (r)
 TIGER Unwin (unw) (u)
 McMurdo (mcm)
 Falkland Islands (fir)
 Zhongshan (zho)
 Buckland Park (bkp)
 South Pole Station (sps)
 Dome C East (dce)
"""

class SouthRadar():

    SINGLE_TO_ABBRV = {'h': 'hal', 'j': 'sys', 'd': 'san', 'n': 'sye', 'p': 'ker', 'r': 'tig', 'u': 'unw'}
    SINGLE_EXTENSIONS = {'h': 'fit', 'j': 'fit', 'd': 'fit',
                         'n': 'fit', 'p': 'fit', 'r': 'fit', 'u': 'fit'}

    ABBRV_EXTENSIONS = {'bpk': 'fitacf', 'dce': 'fitacf', 'fir': 'fitacf',
                        'hal': 'fitacf', 'ker': 'fitacf', 'san': 'fitacf',
                        'sye': 'fitacf', 'sys': 'fitacf', 'tig': 'fitacf',
                        'unw': 'fitacf', 'zho': 'fitacf'}
    CHANNEL_ONE_EXTENSIONS = {'mcm.a': 'fitacf', 'sps.a': 'fitacf'}
    CHANNEL_TWO_EXTENSIONS = {'mcm.b': 'fitacf', 'sps.b': 'fitacf'}
    CHANNEL_THREE_EXTENSIONS = {'mcm.c': 'fitacf', 'sps.c': 'fitacf'}
    CHANNEL_FOUR_EXTENSIONS =  {'mcm.d': 'fitacf', 'sps.d': 'fitacf'}

"""
 Notheren Hemisphere Radar Extensions:
 Goose Bay (gbr) (g)
 Kapuskasing (kap) (k)
 Saskatoon (sas) (t)
 Iceland West (sto) (w) - Stokkseyri
 CUTLASS Finland (han) (f) - Hankasalmi
 CUTLASS Iceland East (pyk) (e) - pykkvibaer
 Kodiak (kod) (a)
 Prince George (pgr) (b)
 King Salmon (ksr) (c)
 Wallops Island (wal)
 Rankin Inlet (rkn)
 Hokkaido East (hok)
 Hokkaido West (hwk)
 Inuvik (inv)
 Clyde River (cly)
 Chritmas Valley East (cve)
 Christmas Valley West (cvw)
 Fort Hayes West (fhw)
 Fort Hayes East (fhe)
 Blackstone (bks)
 Adak Island East (ade)
 Adak Island West (adw)
 Longyearbyen (lyr)
 Schefferville (sch) - No longer operational (still used in the convection map process for older data)
"""

# TODO: EXTENSIONS should be put some where else... RADAR constants?

class NorthRadar():
    EXTENSIONS = ['fit','fitacf','lmfit2']
    RADAR_ABBRV = ['ade', 'adw', 'bks',
                   'cve', 'cvw', 'cly',
                   'fhe', 'fhw', 'gbr',
                   'han', 'hok', 'hkw',
                   'inv', 'kap', 'ksr',
                   'lyr', 'pyk', 'pgr',
                   'rkn', 'sas', 'sch',
                   'sto', 'wal', 'ksr',
                   'kod']
    CHANNEL_ONE_ABBRV = ['ksr.a', 'ade.a', 'adw.a']
    CHANNEL_TWO_ABBRV = ['ksr.b', 'ade.b', 'adw.b']
    CHANNEL_THREE_ABBRV = ['kod.c']
    CHANNEL_FOUR_ABBRV = ['kod.d']

    SINGLE_TO_ABBRV = {'g': 'gbr', 'k': 'kap', 't': 'sas',
                       'w': 'sto', 'f': 'han', 'e': 'pyk',
                       'a': 'kod', 'b': 'pgr', 'c': 'ksr'}
    SINGLE_EXTENSIONS = {'g': 'fit', 'k': 'fit', 't': 'fit', 'w': 'fit',
                         'f': 'fit', 'e': 'fit', 'a': 'fit', 'b': 'fit',
                         'c':'fit'}
    ABBRV_EXTENSIONS = {'ade':'fitacf', 'adw':'fitacf', 'bks':'fitacf',
                        'cve':'fitacf', 'cvw':'fitacf', 'cly':'fitacf',
                        'fhe':'fitacf', 'fhw':'fitacf', 'gbr':'fitacf',
                        'han':'fitacf', 'hok':'fitacf', 'hkw':'fitacf',
                        'inv':'fitacf', 'kap':'fitacf', 'ksr':'fitacf',
                        'lyr':'fitacf', 'pyk':'fitacf', 'pgr':'fitacf',
                        'rkn':'fitacf', 'sas':'fitacf', 'sch':'fitacf',
                        'sto':'fitacf', 'wal':'fitacf', 'ksr':'fitacf',
                        'kod':'fitacf'}
    CHANNEL_ONE_EXTENSIONS = {'ksr.a':'fitacf', 'ade.a':'fitacf', 'adw.a':'fitacf'}
    CHANNEL_TWO_EXTENSIONS = {'ksr.b':'fitacf', 'ade.b':'fitacf', 'adw.b':'fitacf'}
    CHANNEL_THREE_EXTENSIONS = {'kod.c':'fitacf'}
    CHANNEL_FOUR_EXTENSIONS = {'kod.d':'fitacf'}

class CandaianRadar():
    SINGLE_TO_ABBRV = {'t': 'sas',
                       'b': 'pgr'}
    SINGLE_EXTENSIONS = {'t': 'fit',
                         'b': 'fit'}
    ABBRV_EXTENSIONS = {'cly':'fitacf',
                        'inv':'fitacf',
                        'pgr':'fitacf',
                        'rkn':'fitacf',
                        'sas':'fitacf'}

class FileExtensions():

    CONCATINATION = '.C0'
    FITACF = '.fitacf'
    FITCON = 'C.fit'
    FITRED = 'C.fitred'

class ErrorCodes():

    ERROMNIFILE = 1
    ERROMNIBADDATA = 2
    ERRFILENOTFOUND = 3
    ERREMPTYFILE = 4
    ERRRST = 5
