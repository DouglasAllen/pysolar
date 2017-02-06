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

"""
Solar geometry functions

This module contains the most important functions for calculation of the position of the sun.

"""
import datetime
import math

from . import constants
from . import time
from . import radiation

def aberration_correction(dt_list, default=None):
    """
    Given date/time list and optional delta T
    calculates
    a correction for abbereation
    """
    sed = sun_earth_distance(dt_list, default)
    # param sun-earth distance is in astronomical units
    # return -20.4898 / (3600.0 * sed)
    return -0.005691611 / sed

def apparent_solar_longitude(dt_list, default=None):
    """
    Given date/time list and optional delta T
    calculates
    Apparent Solar Longitude in degrees
    """
    tgl = true_geocentric_longitude(dt_list, default)
    dpsi = nutation(dt_list, default)['longitude']
    aberration = aberration_correction(dt_list, default)
    return tgl + dpsi + aberration

def coefficients(dt_list, coeffs, default=None):
    """
    computes a polynomial with time-varying coefficients from the given constant
    coefficients array and the current Julian millennium.
    """
    jem = time.julian_ephemeris_millennium(dt_list, default)
    # jem = (2452930.312847 - 2451545.0) / 365250.0
    result = []

    for group in coeffs:
        count = 0.0
        tsum = 0.0
        for item in group:
            tsum += float(item[0]) * math.cos(float(item[1]) + float(item[2]) * jem) * 1e8
        #end for
        result.append(tsum)
        count += 1
    #end for
    return result
#end coefficients

def equation_of_equinox(dt_list, default=None):
    """
    Given date/time list and optional delta T
    calculates
    Equation of Equinox in degrees
    """
    delta_psi = nutation(dt_list, default)['longitude']
    epsilon = true_ecliptic_obliquity(dt_list, default)
    cos_eps = math.cos(math.radians(epsilon))
    return delta_psi * cos_eps

def flattened_latitude(latitude):
    """
    Given latitude
    calculates
    """
    tan_lat = math.tan(math.radians(latitude))
    return math.degrees(math.atan(0.99664719 * tan_lat))

def gasa(dt_list, default=None):
    """
    Given date/time list and optional delta T
    calculates
    Greenwich Apparent Sidereal Angle in degress
    """
    mean = gmsa(dt_list, default)
    eqeq = equation_of_equinox(dt_list, default)
    return (mean + eqeq) % 360.0

def gast(dt_list, default=None):
    """
    Given date/time list and optional delta T
    calculates
    Greenwich Apparent Sidereal Time in hours
    """
    return gasa(dt_list, default) / 15.0

def gmsa(dt_list, default=None):
    """
    Given date/time list and optional delta T
    calculates
    Greenwich Mean Sidereal Angle in degrees
    """
    # 280.46061837+ 360.98564736629*(JD-2451545)+0.000387933*T2-T3/38710000
    # This function doesn't agree with Andreas and Reda as well as it should.
    # Works to ~5 sig figs in current unit test
    jec = time.julian_ephemeris_century(dt_list, default)
    jdn = jec * 36525.0
    day_deg = (360.98564736629 * jdn) # 360.98564736629 is old value
    mean_st = day_deg + 280.46061837 + jec * (0.000387933 + jec * -1 / 38710000.0)
    return mean_st % 360

def gmst(dt_list, default=None):
    """
    Given date/time list and optional delta T
    calculates
    Greenwich Mean Sidereal Time in hours
    """
    return gmsa(dt_list, default) / 15.0

def lasa(dt_list, params_list, default=None):
    """
    Given date/time list and optional delta T
    calculates
    Loacal Apparent Sidereal Angle in degrees
    """
    gaa = gasa(dt_list, default)
    lla = params_list[2]
    return (gaa + lla) % 360.0

def last(dt_list, params_list, default=None):
    """
    Given date/time list and optional delta T
    calculates
    Loacal Apparent Sidereal Time in hours
    """
    laa = lasa(dt_list, params_list, default)
    return laa / 15.0

def lmsa(dt_list, params_list, default=None):
    """
    Given date/time list and optional delta T
    calculates
    Loacal Mean Sidereal Angle in degrees
    """
    mean = gmsa(dt_list, default)
    return (mean + params_list[2]) % 360.0

def lmst(dt_list, params_list, default=None):
    """
    Given date/time list and optional delta T
    calculates
    Loacal Mean Sidereal Time in hours
    """
    mean = lmsa(dt_list, params_list, default)
    return mean / 15.0

# Geocentric functions calculate angles relative to the center of the earth.

def geocentric_latitude(dt_list, default=None):
    """
    Given date/time list and optional delta T
    calculates
    Geocentric Latitude of the Sun in degress
    """
    return -1 * heliocentric_latitude(dt_list, default)

def geocentric_declination(dt_list, default=None):
    """
    Given date/time list and optional delta T
    calculates
    Geocentric declination of the Sun in degress
    """
    asl = apparent_solar_longitude(dt_list, default)
    teo = true_ecliptic_obliquity(dt_list, default)
    glat = geocentric_latitude(dt_list, default)
    sin_asl = math.sin(math.radians(asl))
    sin_teo = math.sin(math.radians(teo))
    cos_teo = math.cos(math.radians(teo))
    sin_glat = math.sin(math.radians(glat))
    cos_glat = math.cos(math.radians(glat))
    return math.degrees(math.asin(sin_glat * cos_teo + cos_glat * sin_teo * sin_asl))

def geocentric_right_ascension(dt_list, default=None):
    """
    Given date/time list and optional delta T
    calculates Geocentric Right Ascension in degrees
    """
    asl = apparent_solar_longitude(dt_list, default)
    teo = true_ecliptic_obliquity(dt_list, default)
    glat = geocentric_latitude(dt_list, default)
    sin_asl = math.sin(math.radians(asl))
    cos_asl = math.cos(math.radians(asl))
    sin_teo = math.sin(math.radians(teo))
    cos_teo = math.cos(math.radians(teo))
    tan_glat = math.tan(math.radians(glat))
    return math.degrees(math.atan2((sin_asl * cos_teo - tan_glat * sin_teo), cos_asl)) % 360

def greenwich_hour_angle(dt_list, default=None):
    """
    Given date/time list and optional delta T
    calculates
    Greenwich Hour Angle in degrees
    """
    gaa = gasa(dt_list, default)
    gra = geocentric_right_ascension(dt_list, default)
    return (gaa - gra) % 360

def heliocentric_latitude(dt_list, default=None):
    """
    Given date/time list and optional delta T
    calculates Heliocentric Latitude in degrees

    That based on the Sun as a center.
    The Nautical Almanac gives the Heliocentric positions of all celestial bodies.
    """
    jem = time.julian_ephemeris_millennium(dt_list, default)
    hlc = heliocentric_lat_elements(dt_list, default)
    return math.degrees((hlc[0] + jem * (
        hlc[1] + jem * (
            hlc[2] + jem * (
                hlc[3] + jem * hlc[4])))) / 1e8) % -360.0

def heliocentric_lat_elements(dt_list, default=None):
    """
    Given date/time list and optional delta T
    gets Coefficient terms for Heliocentric Latitude in radians

    That based on the Sun as a center.
    The Nautical Almanac gives the Heliocentric positions of all celestial bodies.
    """
    hlc = coefficients(dt_list, constants.HELIOCENTRIC_LATITUDE_COEFFS, default)
    return hlc

def heliocentric_longitude(dt_list, default=None):
    """
    Given date/time list and optional delta T
    calculates Heliocentric Longitude in degrees
    That based on the Sun as a center.
    The Nautical Almanac gives the Heliocentric positions of all celestial bodies.
    """
    # return math.degrees(
    #     coefficients(dt_list, constants.HELIOCENTRIC_LONGITUDE_COEFFS, default) / 1e8) % 360
    jem = time.julian_ephemeris_millennium(dt_list, default)
    # jem = (2452930.312847 - 2451545.0) / 365250.0
    hlc = heliocentric_lon_elements(dt_list, default)
    return math.degrees(
        (hlc[0] + jem * (
            hlc[1] + jem * (
                hlc[2] + jem * (
                    hlc[3] + jem * (
                        hlc[4] + jem * hlc[5]))))) / 1e8) % 360.0

def heliocentric_lon_elements(dt_list, default=None):
    """
    Given date/time list and optional delta T
    gets Coefficient terms for Heliocentric Longitude in radians

    That based on the Sun as a center.
    The Nautical Almanac gives the Heliocentric positions of all celestial bodies.
    """
    hlc = coefficients(dt_list, constants.HELIOCENTRIC_LONGITUDE_COEFFS, default)
    return hlc

def incidence_angle(dt_list, params_list, default=None):
    """
    Given date/time list, parameter list, and optional delta T
    calculates
    Angle of Incedence in degrees
    """
    slope = params_list[3]
    slope_orientation = params_list[4]
    taa = topocentric_azimuth_angle(dt_list, params_list, default)
    taa_rad = (math.radians(taa))
    tza = topocentric_zenith_angle(dt_list, params_list, default)
    sin_tza = math.sin(math.radians(tza))
    cos_tza = math.cos(math.radians(tza))
    sin_slope = math.sin(math.radians(slope))
    cos_slope = math.cos(math.radians(slope))
    so_rad = math.radians(slope_orientation)

    return math.degrees(
        math.acos(
            cos_tza * cos_slope + sin_slope * sin_tza * math.cos(taa_rad - math.pi - so_rad)))

def local_hour_angle(dt_list, params_list, default=None):
    """
    Given date/time list, parameter list, and optional delta T
    calculates
    Local Hour Angle
    """
    longitude = params_list[2]
    gha = greenwich_hour_angle(dt_list, default)
    return (gha + longitude) % 360

def max_horizontal_parallax(dt_list, default=None):
    """
    Given date/time list and optional delta T
    calculates
    """
    sed = sun_earth_distance(dt_list, default)
    return 8.794 / (3600 / sed)

def mean_ecliptic_obliquity(dt_list, default=None):
    """
    Given date/time list and optional delta T
    calculates
    Mean Ecliptic Obliquity in degrees
    """
    # (84381.448 - 46.815 * TE - 0.00059 * TE2 + 0.001813 * TE3) / 3600
    jec = time.julian_ephemeris_century(dt_list, default)
    return (84381.406 + jec * (
        -46.836769 + jec * (
            -0.0001831 + jec * (
                0.00200340 + jec * (
                    -0.000000576 + jec * -0.0000000434))))) / 3600

def mean_solar_longitude(dt_list, default=None):
    """
    Given date/time list and optional delta T
    calculates
    Mean Geocentric Longitude in degrees
    """
    # 280.4664567+360007.6982779*Tau+0.03032028*Tau2+Tau3/49931-Tau4/15299-Tau5/1988000
    jct = time.julian_century(dt_list, default)

    mgl = 280.4664567 + jct * (
        36000.76982779 + jct * (
            0.0003032028 + jct * (
                1.0 / 49931.0 + jct * (1.0 / -15299.0 + jct * (1.0 / -1988000.0)))))
    return mgl % 360.0

def nutation(dt_list, default=None):
    """
    Given date/time list and optional delta T
    calculates
    Delta Epsilon and Delta Psi in degrees
    """
    jec = time.julian_ephemeris_century(dt_list, default)
    abcd = constants.NUTATION_COEFFICIENTS
    nutation_long = []
    nutation_oblique = []
    coef = constants.aberration_coeffs()
    xdx = list \
      (
          coef[k](jec)
          for k in
          ( # order is important
              'MeanAnomalyOfMoon',
              'MeanAnomalyOfSun',
              'ArgumentOfLatitudeOfMoon',
              'MeanElongationOfMoon',
              'LongitudeOfAscendingNode',
          )
      )
    sin_terms = constants.FAM
    for idx, _idx in enumerate(abcd):
        sigmaxy = 0.0
        for jdx, _jdx in enumerate(xdx):
            sigmaxy += xdx[jdx] * sin_terms[idx][jdx]
        #end for
        nutation_long.append(
            (abcd[idx][0] + (abcd[idx][1] * jec)) * math.sin(math.radians(sigmaxy)))
        nutation_oblique.append(
            (abcd[idx][2] + (abcd[idx][3] * jec)) * math.cos(math.radians(sigmaxy)))

    # 36000000 scales from 0.0001 arcseconds to degrees
    deltas = {'longitude' : sum(
        nutation_long) / 36000000.0, 'obliquity' : sum(nutation_oblique) / 36000000.0}

    return deltas
#end nutation

def projected_axial_distance(params_list):
    """
    Given parameter list with elevation and latitude
    calculates
    a distance correction for
    """
    elevation = params_list[0]
    latitude = params_list[1]
    flat = flattened_latitude(latitude)
    sin_flat = math.sin(math.radians(flat))
    sin_lat = math.sin(math.radians(latitude))
    return 0.99664719 * sin_flat + (elevation * sin_lat / constants.EARTH_RADIUS)

def projected_radial_distance(params_list):
    """
    Given parameter list having elevation and latitude
    calculates
    a distance correction for
    """
    elevation = params_list[0]
    latitude = params_list[1]
    flattened_latitude_rad = math.radians(flattened_latitude(latitude))
    latitude_rad = math.radians(latitude)
    return math.cos(
        flattened_latitude_rad) + (elevation * math.cos(latitude_rad) / constants.EARTH_RADIUS)

def refraction_correction(dt_list, params_list, default=None):
    """
    Given date/time list, parameter list, and optional delta T
    calculates
    a correction or offset of view caused by refraction of Earth
    atmosphere and view angle.
    """
    #function and default values according to original NREL SPA C code
    #http://www.nrel.gov/midc/spa/

    sun_radius = 0.26667
    atmos_refract = 0.5667
    del_e = 0.0
    tea = topocentric_elevation_angle(dt_list, params_list, default)

    # Approximation only valid if sun is not well below horizon
    # This approximation could be improved;
    # see history at https://github.com/pingswept/pysolar/pull/23
    # Better method could come from Auer and Standish [2000]:
    # http://iopscience.iop.org/1538-3881/119/5/2472/pdf/1538-3881_119_5_2472.pdf
    pressure = params_list[6]
    temperature = params_list[5]
    if tea >= -1.0*(sun_radius + atmos_refract):
        arc = pressure * 2.830 * 1.02
        brc = 1010.0 * temperature * 60.0 * math.tan(math.radians(tea + (10.3/(tea + 5.11))))
        del_e = arc / brc

    return del_e

def right_ascension_parallax(dt_list, params_list, default=None):
    """
    Given date/time list, parameter list, and optional delta T
    calculates
    A delta of Right Ascension caused by parallax in degrees
    """
    gsd = geocentric_declination(dt_list, default)
    ehp = max_horizontal_parallax(dt_list, default)
    lha = local_hour_angle(dt_list, params_list, default)

    prd = projected_radial_distance(params_list)
    sin_ehp = math.sin(math.radians(ehp))
    sin_lha = math.sin(math.radians(lha))

    cos_gsd = math.cos(math.radians(gsd))
    cos_lha = math.cos(math.radians(lha))

    return math.degrees(
        math.atan2(-1 * prd * sin_ehp * sin_lha,
                   cos_gsd - prd * sin_ehp * cos_lha))

def sun_earth_distance(dt_list, default=None):
    """
    Given date/time list and optional delta T
    calculates
    """
    jem = time.julian_ephemeris_millennium(dt_list, default)
    rvc = coefficients(dt_list, constants.AU_DISTANCE_COEFFS, default)
    return (rvc[0] + jem * (rvc[1] + jem * (rvc[2] + jem * (rvc[3] + jem * rvc[4]))))  / 1e8

# Topocentric functions calculate angles relative to a location on the surface of the earth.

def topocentric_azimuth_angle(dt_list, params_list, default=None):
    """
    Given date/time list, parameter list, and optional delta T
    calculates
    Topocentric Azimuth Angle in degrees
    Measured eastward from north
    """
    latitude = params_list[1]
    tdec = topocentric_solar_declination(dt_list, params_list, default)
    tlha = topocentric_lha(dt_list, params_list, default)
    cos_tlha = math.cos(math.radians(tlha))
    sin_tlha = math.sin(math.radians(tlha))
    sin_lat = math.sin(math.radians(latitude))
    cos_lat = math.cos(math.radians(latitude))
    sin_lat = math.cos(math.radians(latitude))
    tan_tdec = math.tan(math.radians(tdec))
    ayt = sin_tlha
    bxt = cos_tlha * sin_lat - tan_tdec * cos_lat
    return 180.0 + math.degrees(math.atan2(ayt, bxt)) % 360

def topocentric_elevation_angle(dt_list, params_list, default=None):
    """
    Given date/time list, parameter list, and optional delta T
    calculates
    Topocentric Elevation Angle in degrees
    """
    latitude = params_list[1]
    sin_latitude = math.sin(math.radians(latitude))
    cos_latitude = math.cos(math.radians(latitude))
    tsd = topocentric_solar_declination(dt_list, params_list, default)
    sin_tsd = math.sin(math.radians(tsd))
    cos_tsd = math.sin(math.radians(tsd))
    tlha = topocentric_lha(dt_list, params_list, default)
    cos_tlha = math.cos(math.radians(tlha))
    return math.degrees(
        math.asin(
            (sin_latitude * sin_tsd) + cos_latitude * cos_tsd * cos_tlha))

def topocentric_lha(dt_list, params_list, default=None):
    """
    Given date/time list, parameter list, and optional delta T
    calculates
    Topocentric Local Hour Angle in degrees
    """
    lha = local_hour_angle(dt_list, params_list, default)
    rap = right_ascension_parallax(dt_list, params_list, default)
    return lha - rap

def topocentric_solar_declination(dt_list, params_list, default=None):
    """
    Given date/time list, parameter list, and optional delta T
    calculates
    Topocentric Solar Declination in degerees
    """
    gsd = geocentric_declination(dt_list, default)
    pad = projected_axial_distance(params_list)
    ehp = max_horizontal_parallax(dt_list, default)
    psra = right_ascension_parallax(dt_list, params_list, default)
    lha = local_hour_angle(dt_list, params_list, default)
    sin_ehp = math.sin(math.radians(ehp))
    sin_gsd = math.sin(math.radians(gsd))
    cos_gsd = math.cos(math.radians(gsd))
    pad = projected_axial_distance(params_list)
    cos_psra = math.cos(math.radians(psra))
    cos_lha = math.cos(math.radians(lha))
    ayt = sin_gsd - pad * sin_ehp * cos_psra
    bxt = cos_gsd - (pad * sin_ehp * cos_lha)
    return math.degrees(math.atan2(ayt, bxt))

def topocentric_right_ascension(dt_list, params_list, default=None):
    """
    Given date/time list parameter list and optional delta T
    calculates
    Topocentric Right Ascension in degrees
    """
    psra = right_ascension_parallax(dt_list, params_list, default)
    gsra = geocentric_right_ascension(dt_list, default)
    return psra + gsra

def topocentric_zenith_angle(dt_list, params_list, default=None):
    """
    Given date/time list, parameter list, and optional delta T
    calculates
    Topocentric Zenith Angle in degrees
    """
    tea = topocentric_elevation_angle(dt_list, params_list, default)
    return 90 - tea - refraction_correction(dt_list, params_list, default)

def true_ecliptic_obliquity(dt_list, default=None):
    """
    Given date/time list and optional delta T
    calculates
    True Ecliptic Oblquity in degrees
    """
    mean_eps = mean_ecliptic_obliquity(dt_list, default)
    delta_eps = nutation(dt_list, default)['obliquity']

    return mean_eps + delta_eps

def true_geocentric_longitude(dt_list, default=None):
    """
    Given date/time list and optional delta T
    calculates
    true Geocentric Longitude of the Sun in degress
    """
    return (heliocentric_longitude(dt_list, default) + 180) % 360

def true_solar_longitude(dt_list, default=None):
    """
    Given date/time list and optional delta T
    calculates
    True Solar Longitude in degrees
    """
    hlon = heliocentric_longitude(dt_list, default)
    return (hlon + 180 - 0.000025) % 360.0


def altitude(when, params_list, default=None):
    """
    See also the faster, but less accurate, altitude_fast()
    """
    dt_list = [when.year, when.month, when.day,
               when.hour, when.minute, when.second,
               when.microsecond, 0, 0]
    tea = topocentric_elevation_angle(dt_list, params_list, default)
    rca = refraction_correction(dt_list, params_list, default)
    return tea + rca

def altitude_fast(when, params_list):
    """
    docstring goes here
    """
# expect 19 degrees for solar.altitude(
#     42.364908,-71.112828,datetime.datetime(2007, 2, 18, 20, 13, 1, 130320))
    day = when.utctimetuple().tm_yday
    latitude = params_list[1]
    longitude = params_list[2]
    cos_ha = math.cos(math.radians(hour_angle(when, longitude)))
    cos_dec = math.cos(math.radians(declination(day)))
    sin_dec = math.sin(math.radians(declination(day)))
    cos_lat = math.cos(math.radians(latitude))
    sin_lat = math.sin(math.radians(latitude))
    return math.degrees(math.asin(cos_lat * cos_dec * cos_ha + sin_lat * sin_dec))

def azimuth(when, params_list, default=None):
    """
    docstring goes here
    """
    dt_list = [when.year, when.month, when.day,
               when.hour, when.minute, when.second,
               when.microsecond, 0, 0]
    return 180 - topocentric_azimuth_angle(dt_list, params_list, default)

def azimuth_fast(when, params_list, default=None):
    """
    docstring goes here
    """
    # expect -50 degrees for solar.get_azimuth(
    #     42.364908,-71.112828,datetime.datetime(2007, 2, 18, 20, 18, 0, 0))
    latitude = params_list[1]
    longitude = params_list[2]
    day = when.utctimetuple().tm_yday
    declination_rad = math.radians(declination(day))
    latitude_rad = math.radians(latitude)
    hour_angle_rad = math.radians(hour_angle(when, longitude))
    altitude_rad = math.radians(altitude(when, params_list, default))

    azimuth_rad = math.asin(
        math.cos(declination_rad) * math.sin(hour_angle_rad) / math.cos(altitude_rad))

    if (
            math.cos(
                hour_angle_rad) >= (
                    math.tan(declination_rad) / math.tan(latitude_rad))):
        return math.degrees(azimuth_rad)
    else:
        return 180 - math.degrees(azimuth_rad)

def declination(day):
    """
    The declination of the sun is the angle between
    Earth's equatorial plane and a line between the Earth and the sun.
    The declination of the sun varies between 23.45 degrees and -23.45 degrees,
    hitting zero on the equinoxes and peaking on the solstices.
    """
    return constants.EARTH_AXIS_INCLINATION * math.sin((2 * math.pi / 365.0) * (day - 81))

def equation_of_time(day):
    """
    returns the number of minutes to add to mean solar time to get actual solar time.
    """
    bias = 2 * math.pi / 364.0 * (day - 81)
    return 9.87 * math.sin(2 * bias) - 7.53 * math.cos(bias) - 1.5 * math.sin(bias)

def hour_angle(when, longitude_deg):
    """
    docstring goes here
    """
    sun_time = solar_time(when, longitude_deg)
    return 15 * (12 - sun_time)

def solar_time(when, longitude_deg):
    """
    returns solar time in hours for the specified longitude and time,
    accurate only to the nearest minute.
    """
    when = when.utctimetuple()
    return (
        (when.tm_hour * 60 + when.tm_min + 4 * longitude_deg + equation_of_time(when.tm_yday))
        /
        60
        )

def solar_test(params_list):
    """
    docstring goes here
    """
    latitude_deg = 42.364908
    longitude_deg = -71.112828
    when = datetime.datetime(
        2003, 10, 17, 19, 30, 30, tzinfo=datetime.timezone.utc)
    # dto = (dto - time.EPOCH)
    thirty_minutes = datetime.timedelta(hours=0.5)
    params_list[1] = latitude_deg
    params_list[2] = longitude_deg
    for _idx in range(48):
        timestamp = when.ctime()
        altitude_deg = altitude(when, params_list)
        azimuth_deg = azimuth(when, params_list)
        power = radiation.radiation_direct(when, altitude_deg)
        if altitude_deg > 0:
            print(timestamp, "UTC", altitude_deg, azimuth_deg, power)
        when = when + thirty_minutes
