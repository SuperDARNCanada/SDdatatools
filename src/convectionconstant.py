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
    pass


class OmniConst():
    pass

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
    SINGLE_EXTENSIONS = ['h', 'j', 'd', 'n', 'p', 'r', 'u']

    ABBRV_EXTENSIONS = ['bpk', 'dce', 'fir', 'hal', 'ker', 'san',
                         'sye', 'sys', 'tig', 'unw', 'zho']
    CHANNEL_ONE_EXTENSIONS = ['mcm.a', 'sps.a']
    CHANNEL_TWO_EXTENSIONS = ['mcm.b', 'sps.b']
    CHANNEL_THREE_EXTENSIONS = ['mcm.c', 'sps.c']
    CHANNEL_FOUR_EXTENSIONS =  ['mcm.d', 'sps.d']

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

class NorthRadar():
    SINGLE_TO_ABBRV = {'g': 'gbr', 'k': 'kap', 't': 'sas', 'w': 'sto', 'f': 'han',
                       'e': 'pyk', 'a': 'kod', 'b': 'pgr', 'c': 'ksr'}
    SINGLE_EXTENSIONS = ['g', 'k', 't', 'w', 'f', 'e', 'a', 'b', 'c']
    ABBRV_EXTENSIONS = ['.ade', '.adw', '.bks', '.cve', '.cvw', '.cly', '.fhe', '.fhw',
                         '.gbr', '.han', '.hok', '.hkw', '.inv', '.kap', '.ksr', '.lyr',
                         '.pyk', '.pgr', '.rkn', '.sas', '.sch', '.sto', '.wal']
    CHANNEL_ONE_EXTENSIONS = ['kod.a', 'ade.a', 'adw.a']
    CHANNEL_TWO_EXTENSIONS = ['kod.b', 'ade.b', 'adw.b']
    CHANNEL_THREE_EXTENSIONS = ['kod.c']
    CHANNEL_FOUR_EXTENSIONS =  ['kod.d']

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
