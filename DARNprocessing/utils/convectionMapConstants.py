#!/usr/bin/python

# Copyright 2017 SuperDARN Canada
#
# Author: Marina Schmidt
# Date: 2018-01-31


class RstConst():
    """
    Constants for RST
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


class FileConst():
    """
        Radar constants for file types and compression types
        Constants:
        Supported File types:
            lmfit2
            fitacf
        Supporting compression types:
            gz
            bz2

        EXT: is a dictionary of the compression extension
                with the compression command and options as the value.

        No support to fit files because of the complexity of file format changes and
        radar acronym changes.

    """
    FILE_TYPE = ['fitacf']
    COMPRESSION_TYPES = ['gz', 'bz2']
    EXT = {'gz': 'gzip -df',
           'bz2': 'bzip2 -dfv'}


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
 Dome C North (dcn)
"""


class SouthRadar():
    """
    South radar constants:
        Constants:
            SINGLE_TO_ABBRV: single abbrevations to 3-letter acronyms, used for
                            converting fit to fitacf files
            RADAR_ABBRV: South radar 3-letter acrnyms
    """
    SINGLE_TO_ABBRV = {'h': 'hal', 'j': 'sys', 'd': 'san', 'n': 'sye',
                       'p': 'ker', 'r': 'tig', 'u': 'unw'}
    RADAR_ABBRV = ['bpk', 'dce', 'dcn', 'fir', 'hal', 'ker', 'san', 'sye',
                   'sys', 'tig', 'unw', 'zho', 'mcm', 'sps']


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
 Jiamusi East (jme)
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

    """
    SINGLE_TO_ABBRV = {'g': 'gbr', 'k': 'kap', 't': 'sas', 's': 'sch',
                       'w': 'sto', 'f': 'han', 'e': 'pyk', 'i': 'wal',
                       'a': 'kod', 'b': 'pgr', 'c': 'ksr'}
    RADAR_ABBRV = ['ade', 'adw', 'bks', 'cve', 'cvw', 'cly', 'fhe', 'fhw',
                   'gbr', 'han', 'hok', 'hkw', 'inv', 'jme', 'kap', 'ksr',
                   'kod', 'lyr', 'pyk', 'pgr', 'rkn', 'sas', 'sch', 'sto',
                   'wal']

