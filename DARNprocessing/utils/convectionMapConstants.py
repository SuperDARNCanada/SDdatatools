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

# TODO: these will probably become obsolete in the future as newer methods/options will be used

class RstConst():
    """
    Constatns for RST
        Constants:
            MIN_RANGE: minimum range gate
            VEMAX: Velocity error maximum
    """
    MIN_RANGE = 2
    VEMAX = 1000000


class OmniConst():
    """
    Omni Constants
        Constatns:
            DELAY: the delay between sattalite transmission and earth.
            Set to 10 minutes ... Kathyrn McWilliams suggested this value
    """
    # TODO: look into calculating as mentioned in this website
    # https://omniweb.gsfc.nasa.gov/html/omni2_doc_old.html
    # Delta-t = (X/V) * {[1 + (Y*W)/X]/[1 - Ve*W/V]},
    # where
    # Delta-t is the time shift in seconds,
    # X and Y are GSE X and Y components of the spacecraft position vector, in km,
    # V is the observed solar wind speed in km/s (assumed radial),
    # Ve is the speed of the Earth's orbital motion (30 km/s).
    # W=tan [0.5 * atan (V/428)] is parameter related to the assumed orientation of the phase front relative
    #   to the Earth-sun line.  It is Half-way between corotation geometry and convection geometry.
    DELAY = 600


class RadarConst():
    """
        Radar constants for file types and compression types
        Constants:
        Supported File types:
            lmfit2
            fitacf
        Supporting compression types:
            gz
            bz2

        No support to fit files because of the complexity of file format changes and
        radar acronym changes.

    """
    FILE_TYPE = ['lmfit2', 'fitacf']
    COMPRESSION_TYPES = ['gz', 'bz2']


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
    """
    South radar constants:
        Constants:
            SINGLE_TO_ABBRV: single abbrevations to 3-letter acronyms, used for
                            converting fit to fitacf files
            RADAR_ABBRV: South radar 3-letter acrnyms
        Stereo radar constants:
            CHANNEL_ONE_ABBRV: radars that have channel 'a' extension
                               <may not be needed anymore>
            CHANNEL_TWO_ABBRV: radars that have a channel 'b' extension
            CHANNEL_THREE_ABBRV: radars that have a channel 'c' extension
            CHANNEL_FOUR_ABBRV: radars that have a channel 'd' extension
    """
    SINGLE_TO_ABBRV = {'h': 'hal', 'j': 'sys', 'd': 'san', 'n': 'sye',
                       'p': 'ker', 'r': 'tig', 'u': 'unw'}
    RADAR_ABBRV = ['bpk', 'dce', 'fir',
                   'hal', 'ker', 'san',
                   'sye', 'sys', 'tig',
                   'unw', 'zho', 'mcm',
                   'sps']

    # TODO: delete? may not be needed
    CHANNEL_ONE_ABBRV = ['mcm.a', 'sps.a']
    CHANNEL_TWO_ABBRV = ['mcm.b', 'sps.b']
    CHANNEL_THREE_ABBRV = ['mcm.c', 'sps.c']
    CHANNEL_FOUR_ABBRV = ['mcm.d', 'sps.d']


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
 Schefferville (sch) - No longer operational
 (still used in the convection map process for older data)
"""


class NorthRadar():
    """
    North Radar constants

        Constants:
            SINGLE_TO_ABBRV: single abbrevations to 3-letter acronyms, used for
                            converting fit to fitacf files
            RADAR_ABBRV: North Radar 3-letter acronyms

        Stereo radar constants:
            CHANNEL_ONE_ABBRV: radars that have channel 'a' extension
                               <may not be needed anymore>
            CHANNEL_TWO_ABBRV: radars that have a channel 'b' extension
            CHANNEL_THREE_ABBRV: radars that have a channel 'c' extension
            CHANNEL_FOUR_ABBRV: radars that have a channel 'd' extension

    """
    SINGLE_TO_ABBRV = {'g': 'gbr', 'k': 'kap', 't': 'sas',
                       'w': 'sto', 'f': 'han', 'e': 'pyk',
                       'a': 'kod', 'b': 'pgr', 'c': 'ksr'}
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


"""
Canadian Radars:
    Saskatoon   (sas)
    Rankin Inlet (rkn)
    Inuvik  (inv)
    Prince George (pgr)
    Clyde River (cly)
"""


class CanadianRadar():
    """
    Candian Radar constants

        Constants:
            SINGLE_TO_ABBRV: single abbrevations to 3-letter acronyms, used for
                            converting fit to fitacf files
            RADAR_ABBRV: Canadian Radar 3-letter acronyms
    """
    SINGLE_TO_ABBRV = {'t': 'sas',
                       'b': 'pgr'}
    RADAR_ABBRV = {'cly',
                   'inv',
                   'pgr',
                   'rkn',
                   'sas'}


# TODO: this may not be need anymore
class FileExtensions():
    CONCATINATION = '.C0'
    FITACF = '.fitacf'
    FITCON = 'C.fit'
    FITRED = 'C.fitred'


# TODO: these may not be used anymore as well
class ErrorCodes():
    """
        Error codes that the code can return... but this is not pythonic?
    """
    ERROMNIFILE = 1
    ERROMNIBADDATA = 2
    ERRFILENOTFOUND = 3
    ERREMPTYFILE = 4
    ERRRST = 5
