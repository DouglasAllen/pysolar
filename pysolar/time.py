#    Copyright Brandon Stafford
#
#    This file is part of Pysolar.
#
#    Pysolar is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 3 of the License, or
#    (at your option) any later version.
#
#    Pysolar is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License along
#    with Pysolar. If not, see <http://www.gnu.org/licenses/>.

"""This file contains functions related to time conversion.
"""
import warnings
import math
import datetime
import time as pytime

SECONDS_PER_DAY = 86400
# datetime.datetime(2000, 1, 1, 12, 0, 0, tzinfo=datetime.timezone.utc)
ITALY = 2299161 # /* 1582-10-15 */
DJ00 = 2451545.0
DJC = 36525.0
DJM = 365250.0

def jdn(dt_list):
    """
    Given datetime object returns Julian Day Number as an integer.
    jjs named after Joseph Justice Scalager.
    """
    year = dt_list[0]
    month = dt_list[1]
    day = dt_list[2]

    not_march = month < 3
    if not_march:
        year -= 1
        month += 12

    fr_y = math.floor(year / 100)
    reform = 2 - fr_y + math.floor(fr_y / 4)
    jjs = day + math.floor(30.6001 * (month + 1)) + reform + (
        math.floor(365.25 * (year + 4716)) - 1524)
    if jjs < ITALY:
        jjs -= reform

    return math.floor(jjs)
# end jdn

def ajd(dt_list, default=None):
    """
    Given datetime object returns Astronomical Julian Day.
    Day is from midnight 00:00:00+00:00 with day fractional
    value added.
    """
    jdd = jdn(dt_list)
    if default is None:
        del_t = delta_t(jdd, default)
    else:
        del_t = default
    # day_decimal = day + (hour - tz + (minute + (second + dut1)/60.0)/60.0)/24.0

    day_fraction = (
        dt_list[3] - dt_list[8] + (
            dt_list[4]  + (
                dt_list[5] + dt_list[6] / 1e6 + dt_list[7]) / 60.0) / 60.0) / 24.0
    return jdd + day_fraction - 0.5 + del_t / 86400.0
# end ajd

def cal(julian):
    """
    given julian day number
    calculate gregorian calendar date
    note: only needed to find delta_t so far
    """
    if julian == 0.0:
        mon = 12
        day = 31.5
        year = 1899
        return [year, mon, day]
    julian -= 2415020.0
    dla = julian + 0.5
    inc = math.floor(dla)
    fix = dla - inc
    if fix == 1:
        fix = 0
        inc += 1

    if inc > -115860.0:
        adj = math.floor((inc / 36524.25) + 0.99835726) + 14
        inc += 1 + adj - math.floor(adj / 4.0)

    bac = math.floor((inc / 365.25) + 0.802601)
    ced = inc - math.floor((365.25 * bac) + 0.750001) + 416
    ghi = math.floor(ced / 30.6001)
    mon = int(ghi - 1)
    day = ced - math.floor(30.6001  *ghi) + fix
    year = int(bac + 1899)

    if ghi > 13.5:
        mon = int(ghi - 13)
    if mon < 2.5:
        year = int(bac + 1900)
    if year < 1:
        year -= 1
    return [year, mon, day]


# add to datetime.datetime.toordinal() to get Julian day number
# math.floor(JD − 1721424.5)
JULIAN_DAY_OFFSET = 1721425 - 0.5

# number of days to add to datetime.datetime.timestamp() / seconds_per_day
# to agree with datetime.datetime.toordinal()
GREGORIAN_DAY_OFFSET = 719163

# EPOCH Julian day number works out to be
# JULIAN_DAY_OFFSET + GREGORIAN_DAY_OFFSET
UNIX_EPOCH_IN_CJD = 2440587.5
EPOCH = datetime.datetime(1970, 1, 1, tzinfo=datetime.timezone.utc)

def delta_t(jd0, default=None):
    """
    Given a julian day returns a suitable value for delta_t
    if no default value is given otherwise use the value given
    as the delta t
    """
    dt_list = cal(jd0)
    # now = now.utctimetuple()
    year, month = dt_list[0], dt_list[1]
    if default != None:
        return default
    if default == 0:
        return 0
    if default != 0 or None:
        if year < DELTA_T_BASE_YEAR:
            year = DELTA_T_BASE_YEAR
            month = 1
        elif year == DELTA_T_BASE_YEAR:
            month = max(0, month - DELTA_T_BASE_MONTH) + 1
        elif year >= DELTA_T_BASE_YEAR + len(DELTA_T):
            year = DELTA_T_BASE_YEAR + len(DELTA_T) - 1
        #end if
        if year == DELTA_T_BASE_YEAR + len(DELTA_T) - 1:
            month = min(month, len(DELTA_T[year - DELTA_T_BASE_YEAR]))
        #end if
        return DELTA_T[year - DELTA_T_BASE_YEAR][month - 1]
          # don't bother doing any fancy interpolation
    #end if
    return None
#end get_delta_t

def timestamp_ymd(dt_list):
    """
    Given date/time list returns total seconds for year, month, and day
    """
    # just get seconds sum for year month and day as we don't want to
    # complicate this by rewriting C code. Too much work.
    return pytime.mktime((dt_list[0], dt_list[1], dt_list[2], 0, 0, 0, -1, -1, -1))

def timestamp_hms(dt_list, default=None):
    """
    Given date/time list returns total seconds for hours, minutes, and seconds
    """
    secs = dt_list[3] * 3600 + dt_list[4] * 60 + dt_list[5] + dt_list[6] / 1e6
    dt1 = delta_t(dt_list, default)
    return secs + dt1

def timestamp(dt_list, default=None):
    """
    Given date/time list returns POSIX timestamp as a float
    in order to work on python 3.2
    cloned from https://hg.python.org/cpython/file/3.5/Lib/datetime.py
    """
    ymd_secs = timestamp_ymd(dt_list)
    hmsms_secs = timestamp_hms(dt_list, default)

    # Return POSIX timestamp as float
    return ymd_secs + hmsms_secs

def julian_day(dt_list, default=None):
    """
    Given a datetime list returns the UT Julian day number
    (including fraction of a day) corresponding to
    the specified date/time. This version assumes the proleptic Gregorian calender;
    trying to adjust for pre-Gregorian dates/times seems pointless now the changeover
    happened over such wildly varying times in different regions.
    """

    # return timestamp(dt_list) / 86400.0 + 2440587.5
    return ajd(dt_list, default)
#end get_julian_solar_day

def julian_ephemeris_day(dt_list, default=None):
    """
    Given a datetime list  returns the TT Julian day number
    (including fraction of a day) corresponding to
    the specified date/time. This version assumes the proleptic Gregorian calender;
    trying to adjust for pre-Gregorian dates/times seems pointless now the changeover
    happened over such wildly varying times in different regions.
    """
    return julian_day(dt_list, default)
#end get_julian_ephemeris_day

def julian_century(julian):
    """ Convert julian to fractional century """
    return (julian - DJ00) / 36525.0

def julian_ephemeris_millennium(julian):
    """ Convert julian to fractional millennium """
    jec = julian_century(julian)
    return jec / 10


 # seconds to add to TAI to get TT
TT_OFFSET = 32.184

#+
# Table of leap-seconds (to date) taken from Wikipedia
# <https://en.wikipedia.org/wiki/Leap_second>.
#-
LEAP_SECONDS_BASE_YEAR = 1972

LEAP_SECONDS_ADJUSTMENTS = \
    [ # two entries per year starting from 1972, first for 23:59:59 June 30,
      # second for 23:59:59 December 31. +1 indicates that 23:59:60 follows,
      # -1 indicates that 23:59:59 does not exist, not that the latter has ever occurred.
        (+1, +1), # 1972 message: 'C0330:Wrong hanging indentation (add 2 spaces).'
        (0, +1), # 1973
        (0, +1), # 1974
        (0, +1), # 1975
        (0, +1), # 1976
        (0, +1), # 1977
        (0, +1), # 1978
        (0, +1), # 1979
        (0, 0), # 1980
        (+1, 0), # 1981
        (+1, 0), # 1982
        (+1, 0), # 1983
        (0, 0), # 1984
        (+1, 0), # 1985
        (0, 0), # 1986
        (0, +1), # 1987
        (0, 0), # 1988
        (0, +1), # 1989
        (0, +1), # 1990
        (0, 0), # 1991
        (+1, 0), # 1992
        (+1, 0), # 1993
        (+1, 0), # 1994
        (0, +1), # 1995
        (0, 0), # 1996
        (+1, 0), # 1997
        (0, +1), # 1998
        (0, 0), # 1999
        (0, 0), # 2000
        (0, 0), # 2001
        (0, 0), # 2002
        (0, 0), # 2003
        (0, 0), # 2004
        (0, +1), # 2005
        (0, 0), # 2006
        (0, 0), # 2007
        (0, +1), # 2008
        (0, 0), # 2009
        (0, 0), # 2010
        (0, 0), # 2011
        (+1, 0), # 2012
        (0, 0), # 2013
        (0, 0), # 2014
        (+1, 0), # 2015
        (+1, 0), # 2016
    ]

def leap_seconds(dt_list):
    """
    Given datetime list returns adjustment to be added to UTC
    at the specified datetime to produce TAI.
    """
    # now = now.utctimetuple()
    adj = 10 # as decreed from 1972
    year = LEAP_SECONDS_BASE_YEAR
    monin = dt_list[1]
    yin = dt_list[0]
    while True:
        if year > yin:
            break
        if year - LEAP_SECONDS_BASE_YEAR >= len(LEAP_SECONDS_ADJUSTMENTS):
            if (
                    yin - LEAP_SECONDS_BASE_YEAR > len(LEAP_SECONDS_ADJUSTMENTS)
                    or
                    yin - LEAP_SECONDS_BASE_YEAR == len(LEAP_SECONDS_ADJUSTMENTS)
                    and
                    monin > 6
            ):
                warnings.warn \
                  (
                      "I don't know about leap seconds after %d"
                      %
                      (LEAP_SECONDS_BASE_YEAR + len(LEAP_SECONDS_ADJUSTMENTS) - 1)
                  )
            #end if
            break
        #end if
        entry = LEAP_SECONDS_ADJUSTMENTS[year - LEAP_SECONDS_BASE_YEAR]
        if year == yin:
            if monin > 6:
                adj += entry[0]
            #end if
            break
        #end if
        adj += entry[0] + entry[1]
        year += 1
    #end while
    return adj
#end get_leap_seconds

# table of values to add to UT1 to get TT (to date), generated by util/get_delta_t script
DELTA_T_BASE_YEAR = 1973

DELTA_T_BASE_MONTH = 2

DELTA_T = \
  [
      [ # 1973
          43.4724, # 2
          43.5648, # 3
          43.6737, # 4
          43.7782, # 5
          43.8763, # 6
          43.9562, # 7
          44.0315, # 8
          44.1132, # 9
          44.1982, # 10
          44.2952, # 11
          44.3936, # 12
      ],
      [ # 1974
          44.4841, # 1
          44.5646, # 2
          44.6425, # 3
          44.7386, # 4
          44.8370, # 5
          44.9302, # 6
          44.9986, # 7
          45.0584, # 8
          45.1284, # 9
          45.2064, # 10
          45.2980, # 11
          45.3897, # 12
      ],
      [ # 1975
          45.4761, # 1
          45.5633, # 2
          45.6450, # 3
          45.7375, # 4
          45.8284, # 5
          45.9133, # 6
          45.9820, # 7
          46.0408, # 8
          46.1067, # 9
          46.1825, # 10
          46.2789, # 11
          46.3713, # 12
      ],
      [ # 1976
          46.4567, # 1
          46.5445, # 2
          46.6311, # 3
          46.7302, # 4
          46.8284, # 5
          46.9247, # 6
          46.9970, # 7
          47.0709, # 8
          47.1451, # 9
          47.2362, # 10
          47.3413, # 11
          47.4319, # 12
      ],
      [ # 1977
          47.5214, # 1
          47.6049, # 2
          47.6837, # 3
          47.7781, # 4
          47.8771, # 5
          47.9687, # 6
          48.0348, # 7
          48.0942, # 8
          48.1608, # 9
          48.2460, # 10
          48.3439, # 11
          48.4355, # 12
      ],
      [ # 1978
          48.5344, # 1
          48.6325, # 2
          48.7294, # 3
          48.8365, # 4
          48.9353, # 5
          49.0319, # 6
          49.1013, # 7
          49.1591, # 8
          49.2286, # 9
          49.3070, # 10
          49.4018, # 11
          49.4945, # 12
      ],
      [ # 1979
          49.5862, # 1
          49.6805, # 2
          49.7602, # 3
          49.8556, # 4
          49.9489, # 5
          50.0347, # 6
          50.1019, # 7
          50.1622, # 8
          50.2260, # 9
          50.2968, # 10
          50.3831, # 11
          50.4599, # 12
      ],
      [ # 1980
          50.5387, # 1
          50.6161, # 2
          50.6866, # 3
          50.7658, # 4
          50.8454, # 5
          50.9187, # 6
          50.9761, # 7
          51.0278, # 8
          51.0843, # 9
          51.1538, # 10
          51.2319, # 11
          51.3063, # 12
      ],
      [ # 1981
          51.3808, # 1
          51.4526, # 2
          51.5160, # 3
          51.5985, # 4
          51.6809, # 5
          51.7573, # 6
          51.8133, # 7
          51.8532, # 8
          51.9014, # 9
          51.9603, # 10
          52.0328, # 11
          52.0985, # 12
      ],
      [ # 1982
          52.1668, # 1
          52.2316, # 2
          52.2938, # 3
          52.3680, # 4
          52.4465, # 5
          52.5180, # 6
          52.5752, # 7
          52.6178, # 8
          52.6668, # 9
          52.7340, # 10
          52.8056, # 11
          52.8792, # 12
      ],
      [ # 1983
          52.9565, # 1
          53.0445, # 2
          53.1268, # 3
          53.2197, # 4
          53.3024, # 5
          53.3747, # 6
          53.4335, # 7
          53.4778, # 8
          53.5300, # 9
          53.5845, # 10
          53.6523, # 11
          53.7256, # 12
      ],
      [ # 1984
          53.7882, # 1
          53.8367, # 2
          53.8830, # 3
          53.9443, # 4
          54.0042, # 5
          54.0536, # 6
          54.0856, # 7
          54.1084, # 8
          54.1463, # 9
          54.1914, # 10
          54.2452, # 11
          54.2958, # 12
      ],
      [ # 1985
          54.3427, # 1
          54.3911, # 2
          54.4320, # 3
          54.4898, # 4
          54.5456, # 5
          54.5977, # 6
          54.6355, # 7
          54.6532, # 8
          54.6776, # 9
          54.7174, # 10
          54.7741, # 11
          54.8253, # 12
      ],
      [ # 1986
          54.8713, # 1
          54.9161, # 2
          54.9581, # 3
          54.9997, # 4
          55.0476, # 5
          55.0912, # 6
          55.1132, # 7
          55.1328, # 8
          55.1532, # 9
          55.1898, # 10
          55.2416, # 11
          55.2838, # 12
      ],
      [ # 1987
          55.3222, # 1
          55.3613, # 2
          55.4063, # 3
          55.4629, # 4
          55.5111, # 5
          55.5524, # 6
          55.5812, # 7
          55.6004, # 8
          55.6262, # 9
          55.6656, # 10
          55.7168, # 11
          55.7698, # 12
      ],
      [ # 1988
          55.8197, # 1
          55.8615, # 2
          55.9130, # 3
          55.9663, # 4
          56.0220, # 5
          56.0700, # 6
          56.0939, # 7
          56.1105, # 8
          56.1314, # 9
          56.1611, # 10
          56.2068, # 11
          56.2583, # 12
      ],
      [ # 1989
          56.3000, # 1
          56.3399, # 2
          56.3790, # 3
          56.4283, # 4
          56.4804, # 5
          56.5352, # 6
          56.5697, # 7
          56.5983, # 8
          56.6328, # 9
          56.6739, # 10
          56.7332, # 11
          56.7972, # 12
      ],
      [ # 1990
          56.8553, # 1
          56.9111, # 2
          56.9755, # 3
          57.0471, # 4
          57.1136, # 5
          57.1738, # 6
          57.2226, # 7
          57.2597, # 8
          57.3073, # 9
          57.3643, # 10
          57.4334, # 11
          57.5016, # 12
      ],
      [ # 1991
          57.5653, # 1
          57.6333, # 2
          57.6973, # 3
          57.7711, # 4
          57.8407, # 5
          57.9058, # 6
          57.9576, # 7
          57.9975, # 8
          58.0426, # 9
          58.1043, # 10
          58.1679, # 11
          58.2389, # 12
      ],
      [ # 1992
          58.3092, # 1
          58.3833, # 2
          58.4537, # 3
          58.5401, # 4
          58.6228, # 5
          58.6917, # 6
          58.7410, # 7
          58.7836, # 8
          58.8406, # 9
          58.8986, # 10
          58.9714, # 11
          59.0438, # 12
      ],
      [ # 1993
          59.1218, # 1
          59.2003, # 2
          59.2747, # 3
          59.3574, # 4
          59.4434, # 5
          59.5242, # 6
          59.5850, # 7
          59.6344, # 8
          59.6928, # 9
          59.7588, # 10
          59.8386, # 11
          59.9111, # 12
      ],
      [ # 1994
          59.9845, # 1
          60.0564, # 2
          60.1231, # 3
          60.2042, # 4
          60.2804, # 5
          60.3530, # 6
          60.4012, # 7
          60.4440, # 8
          60.4900, # 9
          60.5578, # 10
          60.6324, # 11
          60.7059, # 12
      ],
      [ # 1995
          60.7853, # 1
          60.8664, # 2
          60.9387, # 3
          61.0277, # 4
          61.1103, # 5
          61.1870, # 6
          61.2454, # 7
          61.2881, # 8
          61.3378, # 9
          61.4036, # 10
          61.4760, # 11
          61.5525, # 12
      ],
      [ # 1996
          61.6287, # 1
          61.6846, # 2
          61.7433, # 3
          61.8132, # 4
          61.8823, # 5
          61.9497, # 6
          61.9969, # 7
          62.0343, # 8
          62.0714, # 9
          62.1202, # 10
          62.1810, # 11
          62.2382, # 12
      ],
      [ # 1997
          62.2950, # 1
          62.3506, # 2
          62.3995, # 3
          62.4754, # 4
          62.5463, # 5
          62.6136, # 6
          62.6571, # 7
          62.6942, # 8
          62.7383, # 9
          62.7926, # 10
          62.8567, # 11
          62.9146, # 12
      ],
      [ # 1998
          62.9659, # 1
          63.0217, # 2
          63.0807, # 3
          63.1462, # 4
          63.2053, # 5
          63.2599, # 6
          63.2844, # 7
          63.2961, # 8
          63.3126, # 9
          63.3422, # 10
          63.3871, # 11
          63.4339, # 12
      ],
      [ # 1999
          63.4673, # 1
          63.4979, # 2
          63.5319, # 3
          63.5679, # 4
          63.6104, # 5
          63.6444, # 6
          63.6642, # 7
          63.6739, # 8
          63.6926, # 9
          63.7147, # 10
          63.7518, # 11
          63.7927, # 12
      ],
      [ # 2000
          63.8285, # 1
          63.8557, # 2
          63.8804, # 3
          63.9075, # 4
          63.9393, # 5
          63.9691, # 6
          63.9799, # 7
          63.9833, # 8
          63.9938, # 9
          64.0093, # 10
          64.0400, # 11
          64.0670, # 12
      ],
      [ # 2001
          64.0908, # 1
          64.1068, # 2
          64.1282, # 3
          64.1584, # 4
          64.1833, # 5
          64.2094, # 6
          64.2117, # 7
          64.2073, # 8
          64.2116, # 9
          64.2223, # 10
          64.2500, # 11
          64.2761, # 12
      ],
      [ # 2002
          64.2998, # 1
          64.3192, # 2
          64.3450, # 3
          64.3735, # 4
          64.3943, # 5
          64.4151, # 6
          64.4132, # 7
          64.4118, # 8
          64.4097, # 9
          64.4168, # 10
          64.4329, # 11
          64.4511, # 12
      ],
      [ # 2003
          64.4734, # 1
          64.4893, # 2
          64.5053, # 3
          64.5269, # 4
          64.5471, # 5
          64.5597, # 6
          64.5512, # 7
          64.5371, # 8
          64.5359, # 9
          64.5415, # 10
          64.5544, # 11
          64.5654, # 12
      ],
      [ # 2004
          64.5736, # 1
          64.5891, # 2
          64.6015, # 3
          64.6176, # 4
          64.6374, # 5
          64.6549, # 6
          64.6530, # 7
          64.6379, # 8
          64.6372, # 9
          64.6400, # 10
          64.6543, # 11
          64.6723, # 12
      ],
      [ # 2005
          64.6876, # 1
          64.7052, # 2
          64.7313, # 3
          64.7575, # 4
          64.7811, # 5
          64.8001, # 6
          64.7995, # 7
          64.7876, # 8
          64.7831, # 9
          64.7921, # 10
          64.8096, # 11
          64.8311, # 12
      ],
      [ # 2006
          64.8452, # 1
          64.8597, # 2
          64.8850, # 3
          64.9175, # 4
          64.9480, # 5
          64.9794, # 6
          64.9895, # 7
          65.0028, # 8
          65.0138, # 9
          65.0371, # 10
          65.0773, # 11
          65.1122, # 12
      ],
      [ # 2007
          65.1464, # 1
          65.1833, # 2
          65.2145, # 3
          65.2494, # 4
          65.2921, # 5
          65.3279, # 6
          65.3413, # 7
          65.3452, # 8
          65.3496, # 9
          65.3711, # 10
          65.3972, # 11
          65.4296, # 12
      ],
      [ # 2008
          65.4573, # 1
          65.4868, # 2
          65.5152, # 3
          65.5450, # 4
          65.5781, # 5
          65.6127, # 6
          65.6288, # 7
          65.6370, # 8
          65.6493, # 9
          65.6760, # 10
          65.7097, # 11
          65.7461, # 12
      ],
      [ # 2009
          65.7768, # 1
          65.8025, # 2
          65.8237, # 3
          65.8595, # 4
          65.8973, # 5
          65.9323, # 6
          65.9509, # 7
          65.9534, # 8
          65.9628, # 9
          65.9839, # 10
          66.0147, # 11
          66.0420, # 12
      ],
      [ # 2010
          66.0699, # 1
          66.0961, # 2
          66.1310, # 3
          66.1683, # 4
          66.2072, # 5
          66.2356, # 6
          66.2409, # 7
          66.2335, # 8
          66.2349, # 9
          66.2441, # 10
          66.2751, # 11
          66.3054, # 12
      ],
      [ # 2011
          66.3246, # 1
          66.3406, # 2
          66.3624, # 3
          66.3957, # 4
          66.4289, # 5
          66.4619, # 6
          66.4749, # 7
          66.4751, # 8
          66.4829, # 9
          66.5056, # 10
          66.5383, # 11
          66.5706, # 12
      ],
      [ # 2012
          66.6030, # 1
          66.6340, # 2
          66.6569, # 3
          66.6925, # 4
          66.7289, # 5
          66.7579, # 6
          66.7708, # 7
          66.7740, # 8
          66.7846, # 9
          66.8103, # 10
          66.8400, # 11
          66.8779, # 12
      ],
      [ # 2013
          66.9069, # 1
          66.9443, # 2
          66.9763, # 3
          67.0258, # 4
          67.0716, # 5
          67.1100, # 6
          67.1266, # 7
          67.1331, # 8
          67.1458, # 9
          67.1718, # 10
          67.2091, # 11
          67.2460, # 12
      ],
      [ # 2014
          67.2810, # 1
          67.3136, # 2
          67.3457, # 3
          67.3890, # 4
          67.4318, # 5
          67.4666, # 6
          67.4858, # 7
          67.4989, # 8
          67.5111, # 9
          67.5353, # 10
          67.5711, # 11
          67.6070, # 12
      ],
      [ # 2015
          67.6439, # 1
          67.6765, # 2
          67.7117, # 3
          67.7591, # 4
          67.8012, # 5
          67.8402, # 6
          67.8606, # 7
          67.8822, # 8
          67.9120, # 9
          67.9546, # 10
          68.0055, # 11
          68.0514, # 12
      ],
      [ # 2016
          68.1024, # 1
          68.1577, # 2
          68.2044, # 3
          68.2665, # 4
          68.3188, # 5
          68.3703, # 6
          68.3964, # 7
          68.4094, # 8
          68.4305, # 9
          68.4630, # 10
          68.5078, # 11
          68.5537, # 12
      ],
      [ # 2017
          68.5928 # 1
      ],
  ] # delta_t
