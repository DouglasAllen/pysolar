#!/usr/bin/python3

#    Library for calculating location of the sun

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
""" Tests for time.py and solar.py """
import datetime
import time as pytime
import unittest
from pysolar import solar, elevation, time, constants, util
 # R0902: Too many instance attributes 7 is recommended (solved)
 # R0904: Too many public methods 20 is recommended (solved)
class TestTime(unittest.TestCase):
    """
    Test time methods
    """
    delta_t = 67
    longitude = -105.1786
    latitude = 39.742476 # 39:44:32
    pressure = 820.0 # millibars
    elevation = 1830.14 # meters
    temperature = 11.0 + constants.CELSIUS_OFFSET # kelvin
    surface_slope = 30.0 # Surface slope (measured from the horizontal plane) [degrees]
    surface_azimuth_rotation = -10.0 # Surface azimuth rotation (measured from south to
    # projection of surface normal on horizontal plane, negative east) [degrees]
    params_list = [elevation, latitude, longitude, surface_slope,
                   surface_azimuth_rotation, temperature, pressure]
    lon_offset = longitude / 360.0
    dut1 = datetime.timedelta(seconds=0.0)
    dt_list = [2003, 10, 17, 19, 30, 30, 0, 0, 0]
    def setUp(self):
        # time at MIDC SPA https://www.nrel.gov/midc/solpos/spa.html
        # has no seconds setting so let's consider new test data.
        # changing the docstring to values found in MIDC SPA for expectation tests.
        # below are ways to make adjustments for delta t. But we are using dt_list[7] for now
        # self.dt_list[5] = math.floor(time.get_delta_t(self.dt_list)) + self.dt_list[5]
        # self.dt_list[6] = round((time.get_delta_t(self.dt_list) % 1) * 1e6) + self.dt_list[6]
        return 'Testing pysolar time functions', int(pytime.time())

    def test_delta_ut1(self):
        """
        testing
        see DUT1 http://asa.usno.navy.mil/SecM/Glossary.html#ut1
        MIDC SPA is set to 0 sec DUT1
        """
        # print(self.test_delta_ut1.__doc__)
        print('testing time.py Delta T method')
        dut1 = datetime.timedelta(0)
        self.assertEqual(dut1, self.dut1)

    def test_julian_astronomical(self):
        """
        MIDC SPA https://www.nrel.gov/midc/solpos/spa.html
        Date, Time,
        10/17/2003, 12:30:30
        Julian day, Julian century
        delta t 67
        2452930.312847, 0.037928
        delta t 0
        2452930.312847, 0.037928
        no delta t defaults to current delta t of date
        2452930.313594, 0.037928
        """
        # print(self.test_julian_astronomical.__doc__)
        print('testing time.py Julian Day method')
        jdn = time.jdn(self.dt_list)
        self.assertEqual(2452930, jdn)

        ajd = time.ajd(self.dt_list, self.delta_t)
        self.assertEqual(2452930.313622685, ajd, 6)

        ajd1 = time.ajd(self.dt_list, 0)
        self.assertEqual(2452930.312847222, ajd1, 6)

        ajd2 = time.ajd(self.dt_list)
        self.assertEqual(2452930.3135942305, ajd2, 6)

        jsd = time.julian_day(self.dt_list, self.delta_t)
        self.assertEqual(2452930.313622685, jsd, 6)

        jsd1 = time.julian_day(self.dt_list, 0)
        self.assertEqual(2452930.312847222, jsd1, 6)

        jsd2 = time.julian_day(self.dt_list)
        self.assertEqual(2452930.3135942305, jsd2, 6)

        print('testing time.py Julian Century method')
        jct = time.julian_century(self.dt_list, self.delta_t)
        self.assertEqual(0.037927819922933585, jct, 6)
        self.assertAlmostEqual(0.037928, jct, 6)

        jct1 = time.julian_century(self.dt_list, 0)
        self.assertEqual(0.03792779869191517, jct1, 6)
        self.assertAlmostEqual(0.037928, jct1, 6)

        jct2 = time.julian_century(self.dt_list)
        self.assertEqual(0.0379278191438864, jct2, 6)
        self.assertAlmostEqual(0.037928, jct2, 6)

    def test_julian_ephemeris(self):
        """
        Julian ephemeris day, Julian ephemeris century, Julian ephemeris millennium
        delta t 67
        2452930.313623, 0.037928, 0.003793
        delta t 0
        2452930.312847, 0.037928, 0.003793
        """
        # print(self.test_julian_ephemeris.__doc__)
        print('testing time.py Julian Ephemeris Day method')
        jed = time.julian_ephemeris_day(self.dt_list, self.delta_t)
        self.assertEqual(2452930.313622685, jed, 6)
        self.assertAlmostEqual(2452930.313623, jed, 6)

        jed1 = time.julian_ephemeris_day(self.dt_list, 0)
        self.assertEqual(2452930.312847222, jed1, 6)
        self.assertAlmostEqual(2452930.312847, jed1, 6)

        jed2 = time.julian_ephemeris_day(self.dt_list)
        self.assertEqual(2452930.3135942305, jed2, 6)
        self.assertAlmostEqual(2452930.313594, jed2, 6)

        print('testing time.py Julian Ephemeris Century method')
        jec = time.julian_ephemeris_century(self.dt_list)
        self.assertEqual(0.0379278191438864, jec, 6)
        self.assertAlmostEqual(0.037928, jec, 6)

        jec1 = time.julian_ephemeris_century(self.dt_list, 0)
        self.assertEqual(0.03792779869191517, jec1, 6)
        self.assertAlmostEqual(0.037928, jec1, 6)

        jec2 = time.julian_ephemeris_century(self.dt_list, self.delta_t)
        self.assertEqual(0.037927819922933585, jec2, 6)
        self.assertAlmostEqual(0.037928, jec2, 6)

        print('testing time.py Julian Ephemeris Millennium method')
        jem = time.julian_ephemeris_millennium(self.dt_list, self.delta_t)
        self.assertEqual(0.003792781992293359, jem, 6)
        self.assertAlmostEqual(0.003793, jem, 6)

        jem1 = time.julian_ephemeris_millennium(self.dt_list, 0)
        self.assertEqual(0.003792779869191517, jem1, 6)
        self.assertAlmostEqual(0.003793, jem1, 6)

        jem2 = time.julian_ephemeris_millennium(self.dt_list)
        self.assertEqual(0.0037927819143886397, jem2, 6)
        self.assertAlmostEqual(0.003793, jem2, 6)

        jlon = time.julian_day(self.dt_list, self.delta_t) - self.lon_offset
        self.assertEqual(2452930.605785463, jlon, 6)

        jlon1 = time.julian_day(self.dt_list, 0) - self.lon_offset
        self.assertEqual(2452930.60501, jlon1, 6)

        jlon2 = time.julian_day(self.dt_list) - self.lon_offset
        self.assertEqual(2452930.6057570083, jlon2, 6)

    def test_leap_seconds(self):
        """
        testing Leap seconds
        """
        # print(self.test_leap_seconds.__doc__)
        print('testing time.py Leap Seconds method')
        gls = time.leap_seconds(self.dt_list)
        self.assertEqual(gls, 32)

    def test_ephemeris_to_solar(self):
        """
        testing
        A comparison of Julian Ephemeris day to Julian Day
        This shows a little bit of error creeping in
        """
        # print(self.test_ephemeris_to_solar.__doc__)
        jed1 = time.julian_ephemeris_day(self.dt_list)
        jed1 += self.delta_t / 86400.0
        jsd1 = time.julian_day(self.dt_list)
        test = (jed1 - jsd1) * 86400 - self.delta_t
        self.assertEqual(-1.3113021850585938e-06, test)

    def test_timestamp(self):
        """
        testing Timestamp
        """
        # print(self.test_timestamp.__doc__)
        # print(int(pytime.time())/86400.0 + 2440587.5)
        print('testing time.py Timestamp method')
        tss = time.timestamp(self.dt_list, self.delta_t)
        self.assertEqual(1066437097.0, tss, 6)

        tss1 = time.timestamp(self.dt_list, 0)
        self.assertEqual(1066437030.0, tss1, 6)

        tss2 = time.timestamp(self.dt_list)
        self.assertEqual(1066437094.5415, tss2, 6)

class TestSiderealTime(unittest.TestCase):
    """
    Test sidereal time methods
    """
    delta_t = 67
    longitude = -105.1786
    latitude = 39.742476 # 39:44:32
    pressure = 820.0 # millibars
    elevation = 1830.14 # meters
    temperature = 11.0 + constants.CELSIUS_OFFSET # kelvin
    surface_slope = 30.0 # Surface slope (measured from the horizontal plane) [degrees]
    surface_azimuth_rotation = -10.0 # Surface azimuth rotation (measured from south to
    # projection of surface normal on horizontal plane, negative east) [degrees]
    params_list = [elevation, latitude, longitude, surface_slope,
                   surface_azimuth_rotation, temperature, pressure]
    lon_offset = longitude / 360.0
    dut1 = datetime.timedelta(seconds=0.0)
    dt_list = [2003, 10, 17, 19, 30, 30, 0, 0, 0]
    def setUp(self):
        # time at MIDC SPA https://www.nrel.gov/midc/solpos/spa.html
        # has no seconds setting so let's consider new test data.
        # changing the docstring to values found in MIDC SPA for expectation tests.
        # below are ways to make adjustments for delta t. But we are using dt_list[7] for now
        # self.dt_list[5] = math.floor(time.get_delta_t(self.dt_list)) + self.dt_list[5]
        # self.dt_list[6] = round((time.get_delta_t(self.dt_list) % 1) * 1e6) + self.dt_list[6]
        return 'Testing pysolar time functions', int(pytime.time())

    def test_delta_epsilon(self):
        """
        testing Nutation obliquity
        Date, Time, Nutation obliquity
        delta t 67
        10/17/2003, 12:30:30, 0.001667
        delta t 0
        10/17/2003, 12:30:30, 0.001667
        """
        # print(self.test_delta_epsilon.__doc__)
        print('testing solar.py Delta Epsilon method')
        deps = solar.nutation(self.dt_list, self.delta_t)['obliquity']
        self.assertEqual(0.0016592848763448873, deps, 12)
        # self.assertAlmostEqual(0.001667, deps, 6)

        deps1 = solar.nutation(self.dt_list, 0)['obliquity']
        self.assertEqual(0.0016592816501088399, deps1, 12)
        # self.assertAlmostEqual(0.001667, deps1, 6)

        deps2 = solar.nutation(self.dt_list)['obliquity']
        self.assertEqual(0.0016592847578979105, deps2, 12)
        # self.assertAlmostEqual(0.001667, deps2, 6)

    def test_delta_psi(self):
        """
        testing Nutation longitude
        Date, Time, Nutation longitude
        delta t 67
        10/17/2003, 12:30:30, -0.003998
        delta t 0
        10/17/2003, 12:30:30, -0.003998
        """
        # print(self.test_delta_psi.__doc__)
        print('testing solar.py Delta Psi method')
        dpsi = solar.nutation(self.dt_list, self.delta_t)['longitude']
        self.assertEqual(-0.003987361549780438, dpsi, 12)
        # self.assertAlmostEqual(-0.003998, dpsi, 6)

        dpsi1 = solar.nutation(self.dt_list, 0)['longitude']
        self.assertEqual(-0.00398738273399691, dpsi1, 12)
        # self.assertAlmostEqual(-0.003998, dpsi1, 6)

        dpsi2 = solar.nutation(self.dt_list)['longitude']
        self.assertEqual(-0.003987362327056894, dpsi2, 12)
        self.assertAlmostEqual(-0.003987, dpsi2, 6)

    def test_equation_of_eqinox(self):
        """
        testing
        Equation of equinox = delta psi * cosine epsilon
        delta t 67 and 0 and default
        """
        # print(self.test_equation_of_eqinox.__doc__)
        print('testing solar.py Equation of Equinox method')
        eqeq = solar.equation_of_equinox(self.dt_list, self.delta_t) * 240.0
        self.assertEqual(-0.8783159665591737, eqeq, 15)
        self.assertAlmostEqual(-0.8783159665591737, eqeq, 12)

        eqeq1 = solar.equation_of_equinox(self.dt_list, 0) * 240.0
        self.assertEqual(-0.878320632750602, eqeq1, 15)
        self.assertAlmostEqual(-0.878320632750602, eqeq1, 12)

        eqeq2 = solar.equation_of_equinox(self.dt_list) * 240.0
        self.assertEqual(-0.8783161377678063, eqeq2, 15)
        self.assertAlmostEqual(-0.8783161377678063, eqeq2, 12)

    def test_mean_epsilon(self):
        """
        docs pending
        """
        # print(self.test_mean_epsilon.__doc__)
        print('testing solar.py Mean Epsilon method')
        meps = solar.mean_ecliptic_obliquity(self.dt_list, self.delta_t)
        self.assertEqual(84204.01725304849, meps, 6)
        self.assertAlmostEqual(84204.017253, meps, 6)

        meps1 = solar.mean_ecliptic_obliquity(self.dt_list, 0)
        self.assertEqual(84204.01735224901, meps1, 6)
        self.assertAlmostEqual(84204.017352, meps1, 6)

        meps2 = solar.mean_ecliptic_obliquity(self.dt_list)
        self.assertEqual(84204.01725668853, meps2, 6)
        self.assertAlmostEqual(84204.017257, meps2, 6)

    def test_sidereal_angles(self):
        """
        testing
        with or without delta t on the site calculator
        Mean sidereal time is not effected by delta t
        Date, Time, Greenwich mean sidereal time, Greenwich apparent sidereal time
        delta t 67
        10/17/2003, 12:30:30, 318.515578, 318.511910
        delta t 0
        10/17/2003, 12:30:30, 318.515578, 318.511910
        """
        # print(self.test_sidereal_angles.__doc__)
        print('testing solar.py Greenwich Mean Sideral Time method')
        gmst = solar.gmst(self.dt_list, self.delta_t)
        self.assertEqual(318.79552288219566, gmst, 12)
        # self.assertAlmostEqual(318.515578, gmst, 6)

        gmst1 = solar.gmst(self.dt_list, 0)
        self.assertEqual(318.5155918879318, gmst1, 12)
        # self.assertAlmostEqual(318.515578, gmst1, 6)

        gmst2 = solar.gmst(self.dt_list)
        self.assertEqual(318.785251144378, gmst2, 12)
        self.assertAlmostEqual(318.785251, gmst2, 6)

        print('testing solar.py Greenwich Apparent Sidereal Time method')
        gast = solar.gast(self.dt_list, self.delta_t)
        self.assertEqual(318.791863232335, gast, 12)
        # self.assertAlmostEqual(318.511910, gast, 6)

        gast1 = solar.gast(self.dt_list, 0)
        self.assertEqual(318.51193221862866, gast1, 12)
        # self.assertAlmostEqual(318.511910, gast1, 6)

        gast2 = solar.gast(self.dt_list)
        self.assertEqual(318.78159149380394, gast2, 12)
        self.assertAlmostEqual(318.781591, gast2, 6)

        print('testing solar.py Local Mean Sidereal Time method')
        lmst = solar.lmst(self.dt_list, self.params_list, self.delta_t)
        self.assertEqual(348.79552288219566, lmst, 12)

        lmst1 = solar.lmst(self.dt_list, self.params_list, 0)
        self.assertEqual(348.5155918879318, lmst1, 12)

        lmst2 = solar.lmst(self.dt_list, self.params_list)
        self.assertEqual(348.785251144378, lmst2, 12)

        print('testing solar.py Local Apparent Sidereal Time method')
        last = solar.last(self.dt_list, self.params_list, self.delta_t)
        self.assertEqual(348.791863232335, last, 12)

        last1 = solar.last(self.dt_list, self.params_list, 0)
        self.assertEqual(348.51193221862866, last1, 12)

        last2 = solar.last(self.dt_list, self.params_list)
        self.assertEqual(348.78159149380394, last2, 12)

class TestHeliocentricSolar(unittest.TestCase):
    """
    Test heliocentric methods
    """
    longitude = -105.1786 # -105:
    lon_offset = longitude / 360.0
    latitude = 39.742476 # 39:44:32
    pressure = 82000.0 # pascals
    elevation = 1830.14 # meters
    temperature = 11.0 + constants.CELSIUS_OFFSET # kelvin
    surface_slope = 30.0 # Surface slope (measured from the horizontal plane) [degrees]
    surface_azimuth_rotation = -10.0 # Surface azimuth rotation (measured from south to
    # projection of surface normal on horizontal plane, negative east) [degrees]
    dt_list = [2003, 10, 17, 19, 30, 30, 0, 0, 0]
    delta_t = 67
    params_list = [elevation, latitude, longitude, surface_slope,
                   surface_azimuth_rotation, temperature, pressure]
    def setup(self):
        """
        'Testing pysolar helio functions'
        """
        return print(self.setup.__doc__)

    def test_lo0_to_lo5(self):
        """
        test each longitude term Element
        """
        print('testing solar.py Heliocentric Longitude Terms method')
        l00 = solar.heliocentric_lon_elements(self.dt_list, 0)[0]
        l01 = solar.heliocentric_lon_elements(self.dt_list, 0)[1]
        l02 = solar.heliocentric_lon_elements(self.dt_list, 0)[2]
        l03 = solar.heliocentric_lon_elements(self.dt_list, 0)[3]
        l04 = solar.heliocentric_lon_elements(self.dt_list, 0)[4]
        l05 = solar.heliocentric_lon_elements(self.dt_list, 0)[5]
        self.assertEqual(1.7206761295918584, l00, 12)
        self.assertEqual(6283.320106689305, l01, 12)
        self.assertEqual(0.0006137595190144218, l02, 12)
        self.assertEqual(-2.690138511587399e-07, l03, 12)
        self.assertEqual(-1.2093960852868582e-06, l04, 12)
        self.assertEqual(-8.79323698930542e-09, l05, 12)

    def test_heliocentric_longitude(self):
        """
        testing Heliocentric longitude
        Date 10/17/2003
        Time 12:30:30
        delta t = 67
        Heliocentric longitude 24.018262
        delta t = 0
        Heliocentric longitude 24.017492
        """
        # print(self.test_heliocentric_longitude.__doc__)
        print('testing solar.py Heliocentric longitude method')
        # data from PDF
        # hlc = [1.72067561526586, 6283.32010650051147, 0.00061368682493,
         #       -0.00000026902819, -0.00000121279536, -0.00000000999999]
        # jem = (2452930.312847 - 2451545.0) / 365250.0
        # hlcs = hlc[0] + jem * (
        #     hlc[1] + jem * (hlc[2] + jem * (hlc[2] + jem * (hlc[4] + jem * hlc[5]))))
        hlon = solar.heliocentric_longitude(self.dt_list, self.delta_t)
        self.assertEqual(25.551939581155224, hlon, 12)
        # self.assertAlmostEqual(24.018235, hlon, 6)

        hlon1 = solar.heliocentric_longitude(self.dt_list, 0)
        self.assertEqual(25.551926150758376, hlon1, 12)
        # self.assertAlmostEqual(24.017492, hlon1, 6)
        # jem = time.julian_ephemeris_millennium(self.dt_list, 0)
        # print(jem * 365250 + 2451545.0)
        # print(hlc)
        # hlone = solar.heliocentric_lon_elements(self.dt_list, 0)
        # print(hlone)
        # print(hlcs % 360.0)
        # print(hlon1 % 360.0)

        hlon2 = solar.heliocentric_longitude(self.dt_list)
        self.assertEqual(25.551939088342525, hlon2, 12)
        self.assertAlmostEqual(25.551939, hlon2, 6)

    def test_heliocentric_latitude(self):
        """
        testing Heliocentric latitude
        Date 10/17/2003
        Time 12:30:30
        delta t = 67
        Heliocentric latitude  -0.000101
        delta t = 0
        Heliocentric latitude  -0.000101
        """
        # print(self.heliocentric_latitude.__doc__)
        print('testing solar.py Heliocentric Latitude method')
        hlat = solar.heliocentric_latitude(self.dt_list, self.delta_t)
        self.assertEqual(-1.7637728852017975e-06, hlat, 12)
        # self.assertAlmostEqual(-0.000101, hlat, 6)

        hlat1 = solar.heliocentric_latitude(self.dt_list, 0)
        self.assertEqual(-1.763521346957271e-06, hlat1, 12)
        # self.assertAlmostEqual(-0.000101, hlat1, 6)

        hlat2 = solar.heliocentric_latitude(self.dt_list)
        self.assertEqual(-1.7637636566742287e-06, hlat2, 12)
        self.assertAlmostEqual(-1.763764e-06, hlat2, 6)

class TestGeocentricSolar(unittest.TestCase):
    """
    Test solar and time methods
    """
    longitude = -105.1786 # -105:
    lon_offset = longitude / 360.0
    latitude = 39.742476 # 39:44:32
    pressure = 82000.0 # pascals
    elevation = 1830.14 # meters
    temperature = 11.0 + constants.CELSIUS_OFFSET # kelvin
    surface_slope = 30.0 # Surface slope (measured from the horizontal plane) [degrees]
    surface_azimuth_rotation = -10.0 # Surface azimuth rotation (measured from south to
    # projection of surface normal on horizontal plane, negative east) [degrees]
    dt_list = [2003, 10, 17, 19, 30, 30, 0, 0, 0]
    delta_t = 67
    params_list = [elevation, latitude, longitude, surface_slope,
                   surface_azimuth_rotation, temperature, pressure]

    def test_geo_lat_lon(self):
        """
        testing
        Date, Time
        10/17/2003, 12:30:30
        Geocentric longitude, Geocentric latitude
        delta t 67
        204.018262, 0.000101
        delta t 0
        204.017492, 0.000101
        """
        # print(self.test_geo_lat_lon.__doc__)
        print('testing solar.py Geocentric Longitude method')
        glon = solar.geocentric_longitude(self.dt_list, self.delta_t)
        self.assertEqual(205.55193958115524, glon, 12)
        # self.assertAlmostEqual(204.018235, glon, 6)

        glon1 = solar.geocentric_longitude(self.dt_list, 0)
        self.assertEqual(205.5519261507584, glon1, 12)
        # self.assertAlmostEqual(204.017492, glon1, 6)

        glon2 = solar.geocentric_longitude(self.dt_list)
        self.assertEqual(205.55193908834252, glon2, 12)
        self.assertAlmostEqual(205.551939, glon2, 6)

        print('testing solar.py Geocentric Latitude')
        glat = solar.geocentric_latitude(self.dt_list, self.delta_t)
        self.assertEqual(1.7637728852017975e-06, glat, 12)
        # self.assertAlmostEqual(0.000101, glat, 6)

        glat1 = solar.geocentric_latitude(self.dt_list, 0)
        self.assertEqual(1.763521346957271e-06, glat1, 12)
        # self.assertAlmostEqual(0.000101, glat1, 6)

        glat2 = solar.geocentric_latitude(self.dt_list)
        self.assertEqual(1.7637636566742287e-06, glat2, 12)
        self.assertAlmostEqual(1.763764e-06, glat2, 6)

    def test_geo_rad_dec(self):
        """
        testing
        Date, Time, Geocentric sun right ascension, Geocentric sun declination
        delta t 67
        10/17/2003, 12:30:30, 202.227408, -9.314340
        delta t 0
        10/17/2003, 12:30:30, 202.226683, -9.314057
        """
        # print(self.test_geo_rad_dec.__doc__)
        print('testing solar.py Geocentric Right Ascension method')
        gsra = solar.geocentric_right_ascension(self.dt_list, self.delta_t)
        self.assertEqual(203.68249439406245, gsra, 12)
        # self.assertAlmostEqual(202.234783, gsra, 5)

        gsra1 = solar.geocentric_right_ascension(self.dt_list, 0)
        self.assertEqual(203.68248167252372, gsra1, 12)
        # self.assertAlmostEqual(202.226683, gsra1, 5)

        gsra2 = solar.geocentric_right_ascension(self.dt_list)
        self.assertEqual(203.6824939272605, gsra2, 12)
        self.assertAlmostEqual(203.682494, gsra2, 6)

        print('testing solar.py Geocentric Declination method')
        gsd = solar.geocentric_declination(self.dt_list, self.delta_t)
        self.assertEqual(-9.856619745423947, gsd, 12)
        # self.assertAlmostEqual(-9.295870, gsd, 6)

        gsd1 = solar.geocentric_declination(self.dt_list, 0)
        self.assertEqual(-9.85661486515095, gsd1, 12)
        # self.assertAlmostEqual(-9.314057, gsd1, 6)

        gsd2 = solar.geocentric_declination(self.dt_list)
        self.assertEqual(-9.856619566348034, gsd2, 12)
        self.assertAlmostEqual(-9.856620, gsd2, 6)

class TestSolar(unittest.TestCase):
    """
    Non Az El Geocentric or Topocentric
    """
    longitude = -105.1786 # -105:
    lon_offset = longitude / 360.0
    latitude = 39.742476 # 39:44:32
    pressure = 82000.0 # pascals
    elevation = 1830.14 # meters
    temperature = 11.0 + constants.CELSIUS_OFFSET # kelvin
    surface_slope = 30.0 # Surface slope (measured from the horizontal plane) [degrees]
    surface_azimuth_rotation = -10.0 # Surface azimuth rotation (measured from south to
    # projection of surface normal on horizontal plane, negative east) [degrees]
    dt_list = [2003, 10, 17, 19, 30, 30, 0, 0, 0]
    delta_t = 67
    params_list = [elevation, latitude, longitude, surface_slope,
                   surface_azimuth_rotation, temperature, pressure]
    def setUp(self):
        # time at MIDC SPA https://www.nrel.gov/midc/solpos/spa.html
        # has no seconds setting so let's consider new test data.
        # changing the docstring to values found in MIDC SPA for expectation tests.
        # Reda & Andreas say that this time is in "Local Standard Time", which they
        # define as 7 hours behind UT (not UTC). Hence the adjustment to convert UT
        # to UTC.
        # print(int(pytime.time()))
        return None

    def test_aberration_correction(self):
        """
        testing
        Date, Time, Aberration correction
        delta t 67
        10/17/2003, 12:30:30, -0.005711
        delta t 0
        10/17/2003, 12:30:30, -0.005711
        """
        # print(self.test_aberration_correction.__doc__)
        print('testing solar.py Aberration Correction method')
        gac = solar.aberration_correction(self.dt_list, self.delta_t)
        self.assertEqual(-0.005711359293251812, gac, 12)
        self.assertAlmostEqual(-0.005711, gac, 6)

        gac1 = solar.aberration_correction(self.dt_list, 0)
        self.assertEqual(-0.0057113580676371465, gac1, 12)
        self.assertAlmostEqual(-0.005711, gac1, 6)

        gac2 = solar.aberration_correction(self.dt_list)
        self.assertEqual(-0.005711359248279383, gac2, 12)
        self.assertAlmostEqual(-0.005711, gac2, 6)

    def test_apparent_sun_longitude(self):
        """
        Date, Time, Apparent sun longitude
        delta t 67
        10/17/2003, 12:30:30, 204.008552
        delta t 0
        10/17/2003, 12:30:30, 204.007782
        """
        # print(self.test_apparent_sun_longitude.__doc__)
        print('testing solar.py Apparent Sun Longitude method')
        asl = solar.apparent_sun_longitude(self.dt_list, self.delta_t)
        self.assertEqual(205.5422408603122, asl, 12)
        # self.assertAlmostEqual(204.008552, asl, 6)

        asl1 = solar.apparent_sun_longitude(self.dt_list, 0)
        self.assertEqual(205.54222740995675, asl1, 12)
        # self.assertAlmostEqual(204.007782, asl1, 6)

        asl2 = solar.apparent_sun_longitude(self.dt_list)
        self.assertEqual(205.5422403667672, asl2, 12)
        self.assertAlmostEqual(205.542240, asl2, 6)

    def test_local_hour_angle(self):
        """
        testing
        Date, Time, Observer hour angle
        delta t 67
        10/17/2003, 12:33:30, 11.856008
        delta t 0
        10/17/2003, 12:30:30, 11.106627
        """
        # print(self.test_local_hour_angle.__doc__)
        print('testing solar.py Local Hour Angle method')
        lha = solar.local_hour_angle(self.dt_list, self.params_list, self.delta_t)
        self.assertEqual(9.930768838272542, lha, 12)
        # self.assertAlmostEqual(11.856008, lha, 6)

        lha1 = solar.local_hour_angle(self.dt_list, self.params_list, 0)
        self.assertEqual(9.65085054610492, lha1, 12)
        # self.assertAlmostEqual(11.106627, lha1, 6)

        lha2 = solar.local_hour_angle(self.dt_list, self.params_list)
        self.assertEqual(9.920497566543418, lha2, 12)
        self.assertAlmostEqual(9.920498, lha2, 6)

    def test_max_horizontal_parallax(self):
        """
        testing
        Date, Time, Sun equatorial horizontal parallax
        delta t 0
        10/17/2003, 12:30:30, 0.002451
        delta t 67
        10/17/2003, 12:30:30, 0.002451
        """
        # print(self.test_max_horizontal_parallax.__doc__)
        print('testing solar.py Equitorial Horizontal Parallax method')
        ehp = solar.max_horizontal_parallax(self.dt_list, self.delta_t)
        self.assertEqual(0.002434331378591894, ehp, 12)
        self.assertAlmostEqual(0.002434, ehp, 6)

        ehp1 = solar.max_horizontal_parallax(self.dt_list, 0)
        self.assertEqual(0.0024343319009811756, ehp1, 12)
        # self.assertAlmostEqual(0.002451, ehp1, 6)

        ehp2 = solar.max_horizontal_parallax(self.dt_list)
        self.assertEqual(0.0024343313977603248, ehp2, 12)
        self.assertAlmostEqual(0.002434, ehp2, 6)

    def test_pressure_with_elevation(self):
        """
        testing Pressure with elevation
        MIDC SPA is not at 12:30
        """
        # print(self.test_pressure_with_elevation.__doc__)
        print('testing solar.py Pressure with Elevation method')
        pwe = elevation.pressure_with_elevation(1567.7)
        self.assertEqual(83855.90227687225, pwe, 12)

    def test_projected_axial_distance(self):
        """
        testing Projected axial distance
        MIDC SPA is not at 12:30
        """
        # print(self.test_projected_axial_distance.__doc__)
        print('testing solar.py Projected Axial Distance method')
        pad = solar.projected_axial_distance(self.params_list)
        self.assertEqual(0.6361121708785658, pad, 12)

    def test_projected_radial_distance(self):
        """
        testing Projected radial distance
        MIDC SPA is not at 12:30
        """
        # print(self.test_projected_radial_distance.__doc__)
        print('testing solar.py Projected Radial Distance method')
        prd = solar.projected_radial_distance(self.params_list)
        self.assertEqual(0.7702006191191089, prd, 12)

    def test_sun_earth_distance(self):
        """
        testing
        Date, Time, Earth radius vector
        delta t 67
        10/17/2003, 12:30:30, 0.996542
        delta t 0
        10/17/2003, 12:30:30, 0.996543
        """
        # print(self.test_sun_earth_distance.__doc__)
        print('testing solar.py Sun Earth Distance method')
        sed = solar.sun_earth_distance(self.dt_list, self.delta_t)
        self.assertEqual(0.9965422973539707, sed, 12)
        self.assertAlmostEqual(0.996542, sed, 6)

        sed1 = solar.sun_earth_distance(self.dt_list, 0)
        self.assertEqual(0.996542511204484, sed1, 12)
        self.assertAlmostEqual(0.996543, sed1, 6)

        sed2 = solar.sun_earth_distance(self.dt_list)
        self.assertEqual(0.9965423052009517, sed2, 12)
        self.assertAlmostEqual(0.996542, sed2, 6)

    def test_temperature_with_elevation(self):
        """
        testing
        Temperature with elevation
        MIDC SPA is not at 12:30
        """
        # print(self.test_temperature_with_elevation.__doc__)
        print('testing solar.py Temperature with Elevation method')
        twe = elevation.temperature_with_elevation(1567.7)
        self.assertEqual(277.95995, twe, 6)

class TestTopocentricSolar(unittest.TestCase):
    """
    Test solar and time methods
    """
    longitude = -105.1786 # -105:
    lon_offset = longitude / 360.0
    latitude = 39.742476 # 39:44:32
    pressure = 820.0 # millibars
    elevation = 1830.14 # meters
    temperature = 11.0 + constants.CELSIUS_OFFSET # kelvin
    surface_slope = 30.0 # Surface slope (measured from the horizontal plane) [degrees]
    surface_azimuth_rotation = -10.0 # Surface azimuth rotation (measured from south to
    # projection of surface normal on horizontal plane, negative east) [degrees]
    dt_list = [2003, 10, 17, 19, 30, 30, 0, 0, 0]
    delta_t = 67
    params_list = [elevation, latitude, longitude, surface_slope,
                   surface_azimuth_rotation, temperature, pressure]

    def test_incidence_angle(self):
        """
        Date, Time, Surface incidence angle
        delta t 67
        10/17/2003, 12:30:30, 25.187000
        delta t 0
        10/17/2003, 12:30:30, 25.187244
        """
        # print(self.test_incidence_angle.__doc__)
        print('testing solar.py Angle of Incedence method')
        aoi = solar.incidence_angle(self.dt_list, self.params_list, self.delta_t)
        self.assertEqual(75.7424240909027, aoi, 12)
        # self.assertAlmostEqual(25.187000, aoi, 6)

        aoi1 = solar.incidence_angle(self.dt_list, self.params_list, 0)
        self.assertEqual(75.69429354254089, aoi1, 12)
        # self.assertAlmostEqual(25.187244, aoi1, 6)

        aoi2 = solar.incidence_angle(self.dt_list, self.params_list)
        self.assertEqual(75.74064846672428, aoi2, 12)
        self.assertAlmostEqual(75.740648, aoi2, 6)

    def test_right_ascension_parallax(self):
        """
        Date, Time, Sun right ascension parallax
        delta t 67
        10/17/2003, 12:30:30, -0.000369
        delta t 0
        10/17/2003, 12:30:30, -0.000369

        """
        # print(self.test_right_ascension_parallax.__doc__)
        print('testing solar.py Right Ascension Parallax method')
        rap = solar.right_ascension_parallax(self.dt_list, self.params_list, self.delta_t)
        self.assertEqual(-0.00032820082412157747, rap, 12)
        # self.assertAlmostEqual(-0.000369, rap, 6)

        rap1 = solar.right_ascension_parallax(self.dt_list, self.params_list, 0)
        self.assertEqual(-0.0003190388529370186, rap1, 12)
        # self.assertAlmostEqual(-0.000369, rap1, 6)

        rap2 = solar.right_ascension_parallax(self.dt_list, self.params_list)
        self.assertEqual(-0.0003278647735803167, rap2, 12)
        self.assertAlmostEqual(-0.000328, rap2, 6)

    def test_topo_right_ascension(self):
        """
        Date, Time, Topocentric sun right ascension
        delta t 67
        10/17/2003, 12:30:30, 202.227039
        delta t 0
        10/17/2003, 12:30:30, 202.226314
        """
        # print(self.test_topo_right_ascension.__doc__)
        print('testing solar.py Topocentric Right Ascension method')
        tsra = solar.topocentric_right_ascension(self.dt_list, self.params_list, self.delta_t)
        self.assertEqual(203.68216619323832, tsra, 12)
        # self.assertAlmostEqual(202.226696, tsra, 6)

        tsra1 = solar.topocentric_right_ascension(self.dt_list, self.params_list, 0)
        self.assertEqual(203.68216263367077, tsra1, 12)
        # self.assertAlmostEqual(202.226314, tsra1, 6)

        tsra2 = solar.topocentric_right_ascension(self.dt_list, self.params_list)
        self.assertEqual(203.68216606248694, tsra2, 12)
        self.assertAlmostEqual(203.682166, tsra2, 6)

    def test_topo_sun_declination(self):
        """
        Date,Time,Topocentric sun declination
        delta t 67
        10/17/2003, 12:30:30, -9.316179
        delta t 0
        10/17/2003, 12:30:30, -9.315895
        """
        # print(self.test_topo_sun_declination.__doc__)
        print('testing solar.py Topocentric Sun Declination method')
        tsd = solar.topocentric_sun_declination(self.dt_list, self.params_list, self.delta_t)
        self.assertEqual(-9.858406541459118, tsd, 12)
        # self.assertAlmostEqual(-9.316179, tsd, 6)

        tsd1 = solar.topocentric_sun_declination(self.dt_list, self.params_list, 0)
        self.assertEqual(-9.858401881731565, tsd1, 12)
        # self.assertAlmostEqual(-9.315895, tsd1, 6)

        tsd2 = solar.topocentric_sun_declination(self.dt_list, self.params_list)
        self.assertEqual(-9.858406370586064, tsd2, 12)
        self.assertAlmostEqual(-9.858406, tsd2, 6)

    def test_topocentric_azimuth_angle(self):
        """
        Date, Time, Top. azimuth angle (eastward from N)
        delta t 67
        10/17/2003, 12:30:30, 194.340241
        delta t 0
        10/17/2003, 12:30:30, 194.341226
        """
        # print(self.test_topocentric_azimuth_angle.__doc__)
        print('testing solar.py Topocentric Azimuth Angle method')
        taa = solar.topocentric_azimuth_angle(self.dt_list, self.params_list, self.delta_t)
        self.assertEqual(190.95447810915962, taa, 12)
        # self.assertAlmostEqual(194.340241, taa, 6)

        taa1 = solar.topocentric_azimuth_angle(self.dt_list, self.params_list, 0)
        self.assertEqual(190.64831398667863, taa1, 12)
        # self.assertAlmostEqual(194.341226, taa1, 6)

        taa2 = solar.topocentric_azimuth_angle(self.dt_list, self.params_list)
        self.assertEqual(190.94324773790171, taa2, 12)
        self.assertAlmostEqual(190.943248, taa2, 6)

    def test_topocentric_lha(self):
        """
        Date, Time, Topocentric local hour angle
        delta t 67
        10/17/2003, 12:30:30, 11.106271
        delta t 0
        10/17/2003, 12:30:30, 11.106996
        """
        # print(self.test_topocentric_lha.__doc__)
        print('testing solar.py Topocentric Local Hour Angle method')
        tlha = solar.topocentric_lha(self.dt_list, self.params_list, self.delta_t)
        self.assertEqual(9.931097039096663, tlha, 12)
        # self.assertAlmostEqual(10.982765, tlha, 6)

        tlha1 = solar.topocentric_lha(self.dt_list, self.params_list, 0)
        self.assertEqual(9.651169584957856, tlha1, 12)
        # self.assertAlmostEqual(11.106996, tlha1, 6)

        tlha2 = solar.topocentric_lha(self.dt_list, self.params_list)
        self.assertEqual(9.920825431316999, tlha2, 12)
        self.assertAlmostEqual(9.920825, tlha2, 6)

    def test_topocentric_zenith_angle(self):
        """
        testing
        Date, Time, Topocentric zenith angle
        delta t 67
        10/17/2003, 12:30:30, 50.111622
        delta t 0
        10/17/2003, 12:30:30, 50.111482
        """
        # print(self.test_topocentric_zenith_angle.__doc__)
        print('testing solar.py Topocentric Zenith Angle method')
        tza = solar.topocentric_zenith_angle(self.dt_list, self.params_list, self.delta_t)
        self.assertAlmostEqual(103.83588836819067, tza, 12)
        # self.assertAlmostEqual(50.088106, tza, 6)

        tza1 = solar.topocentric_zenith_angle(self.dt_list, self.params_list, 0)
        self.assertAlmostEqual(103.84233617382108, tza1, 12)
        # self.assertAlmostEqual(50.111482, tza1, 6)

        tza2 = solar.topocentric_zenith_angle(self.dt_list, self.params_list)
        self.assertAlmostEqual(103.83612818899084, tza2, 12)
        self.assertAlmostEqual(103.836128, tza2, 6)

class TestAzElSolar(unittest.TestCase):
    """
    Tests functions that use when as a time parameter
    """
    longitude = -105.1786 # -105:
    lon_offset = longitude / 360.0
    latitude = 39.742476 # 39:44:32
    pressure = 820.0 # millibars
    elevation = 1830.14 # meters
    temperature = 11.0 + constants.CELSIUS_OFFSET # kelvin
    surface_slope = 30.0 # Surface slope (measured from the horizontal plane) [degrees]
    surface_azimuth_rotation = -10.0 # Surface azimuth rotation (measured from south to
    # projection of surface normal on horizontal plane, negative east) [degrees]
    dt_list = [2003, 10, 17, 19, 30, 30, 0, 0, 0]
    delta_t = 67
    tyn = util.TY_DEFAULT
    amd = util.AM_DEFAULT
    ltf = util.TL_DEFAULT
    spc = util.SC_DEFAULT
    params_list = [elevation, latitude, longitude, surface_slope,
                   surface_azimuth_rotation, temperature, pressure,
                   tyn, amd, ltf, spc]
    when = datetime.datetime(
        2003, 10, 17, 19, 30, 30, tzinfo=datetime.timezone.utc)

    def test_altitude(self):
        """
        testing Altitude Angle
        """
        # print(self.test_altitude.__doc__)
        print('testing solar.py Altitude Angle method')
        alt = solar.altitude(self.when, self.params_list, self.delta_t)
        self.assertEqual(-13.835888368190668, alt, 12)

        alt1 = solar.altitude(self.when, self.params_list, 0)
        self.assertEqual(-13.842336173821083, alt1, 12)

        alt2 = solar.altitude(self.when, self.params_list)
        self.assertEqual(-13.836128188990848, alt2, 12)

    def test_azimuth(self):
        """
        testing Azimuth
        """
        # print(self.test_azimuth.__doc__)
        print('testing solar.py Azimuth Angle method')
        azm = solar.azimuth(self.when, self.params_list, self.delta_t)
        self.assertAlmostEqual(-10.954478109159624, azm, 12)

        azm1 = solar.azimuth(self.when, self.params_list, 0)
        self.assertAlmostEqual(-10.64831398667863, azm1, 12)

        azm2 = solar.azimuth(self.when, self.params_list)
        self.assertAlmostEqual(-10.943247737901714, azm2, 12)

class TestSolarSolar(unittest.TestCase):
    """
    Tests functions that use when as a time parameter
    """
    longitude = -105.1786 # -105:
    lon_offset = longitude / 360.0
    latitude = 39.742476 # 39:44:32
    pressure = 820.0 # millibars
    elevation = 1830.14 # meters
    temperature = 11.0 + constants.CELSIUS_OFFSET # kelvin
    surface_slope = 30.0 # Surface slope (measured from the horizontal plane) [degrees]
    surface_azimuth_rotation = -10.0 # Surface azimuth rotation (measured from south to
    # projection of surface normal on horizontal plane, negative east) [degrees]
    dt_list = [2003, 10, 17, 19, 30, 30, 0, 0, 0]
    delta_t = 67
    tyn = util.TY_DEFAULT
    amd = util.AM_DEFAULT
    ltf = util.TL_DEFAULT
    spc = util.SC_DEFAULT
    params_list = [elevation, latitude, longitude, surface_slope,
                   surface_azimuth_rotation, temperature, pressure,
                   tyn, amd, ltf, spc]
    when = datetime.datetime(
        2003, 10, 17, 19, 30, 30, tzinfo=datetime.timezone.utc)

    def test_solar_test(self):
        """
        doc
        """
        print('testing solar.py Solar Test method')
        solar.solar_test(self.params_list)

class TestUtil(unittest.TestCase):
    """
    Tests functions that use when as a time parameter
    """
    longitude = -105.1786 # -105:
    lon_offset = longitude / 360.0
    latitude = 39.742476 # 39:44:32
    pressure = 820.0 # millibars
    elevation = 1830.14 # meters
    temperature = 11.0 + constants.CELSIUS_OFFSET # kelvin
    surface_slope = 30.0 # Surface slope (measured from the horizontal plane) [degrees]
    surface_azimuth_rotation = -10.0 # Surface azimuth rotation (measured from south to
    # projection of surface normal on horizontal plane, negative east) [degrees]
    dt_list = [2003, 10, 17, 19, 30, 30, 0, 0, 0]
    delta_t = 67
    tyn = util.TY_DEFAULT
    amd = util.AM_DEFAULT
    ltf = util.TL_DEFAULT
    spc = util.SC_DEFAULT
    params_list = [elevation, latitude, longitude, surface_slope,
                   surface_azimuth_rotation, temperature, pressure,
                   tyn, amd, ltf, spc]
    when = datetime.datetime(2003, 10, 17, tzinfo=datetime.timezone.utc)

    def test_sunrise_sunset(self):
        """
        testing
        Date, Time, Local sunrise time
        10/17/2003, 12:30:30, 6.212067
        Date, Time, Local sunset time

        """
        # print(self.test_sunrise_sunset.__doc__)
        print('testing util.py Sunrise Sunset method')
        srs = util.sunrise_sunset(self.when, self.params_list)
        # print(srs)
        rtv = datetime.datetime(
            2003, 10, 17, 13, 21, 59, 486508, tzinfo=datetime.timezone.utc)
        stv = datetime.datetime(
            2003, 10, 18, 0, 10, 3, 617537, tzinfo=datetime.timezone.utc)
        self.assertEqual((rtv, stv), srs)

    def test_sunrise(self):
        """
        testing
        Date, Time, Local sunrise time
        10/17/2003, 12:30:30, 6.212067
        Date, Time, Local sunset time

        """
        # print(self.test_sunrise_sunset.__doc__)
        print('testing util.py Sunrise Time method')
        usr = util.sunrise_time(self.when, self.params_list)
        # print(usr)
        rval = datetime.datetime(
            2003, 10, 17, 13, 21, 59, 486508, tzinfo=datetime.timezone.utc)
        self.assertEqual(rval, usr)

    def test_sunset(self):
        """
        testing
        Date, Time, Local sunrise time
        10/17/2003, 12:30:30, 6.212067
        Date, Time, Local sunset time

        """
        # print(self.test_sunrise_sunset.__doc__)
        print('testing util.py Sunset Time method')
        uss = util.sunset_time(self.when, self.params_list)
        # print(uss)
        sval = datetime.datetime(
            2003, 10, 18, 0, 10, 3, 617537, tzinfo=datetime.timezone.utc)
        self.assertEqual(sval, uss)

if __name__ == "__main__":
    SOLAR = unittest.defaultTestLoader.loadTestsFromTestCase(TestSolar)
    TIME = unittest.defaultTestLoader.loadTestsFromTestCase(TestTime)
    HSOLAR = unittest.defaultTestLoader.loadTestsFromTestCase(TestHeliocentricSolar)
    GSOLAR = unittest.defaultTestLoader.loadTestsFromTestCase(TestGeocentricSolar)
    TSOLAR = unittest.defaultTestLoader.loadTestsFromTestCase(TestTopocentricSolar)
    AESOLAR = unittest.defaultTestLoader.loadTestsFromTestCase(TestAzElSolar)
    SIDEREAL = unittest.defaultTestLoader.loadTestsFromTestCase(TestSiderealTime)
    UTIL = unittest.defaultTestLoader.loadTestsFromTestCase(TestUtil)
    INSOLAR = unittest.defaultTestLoader.loadTestsFromTestCase(TestSolarSolar)
    #unittest.TextTestRunner(verbosity=2).run(TIME)
    #unittest.TextTestRunner(verbosity=2).run(HSOLAR)
    #unittest.TextTestRunner(verbosity=2).run(GSOLAR)
    #unittest.TextTestRunner(verbosity=2).run(SIDEREAL)
    #unittest.TextTestRunner(verbosity=2).run(SOLAR)
    #unittest.TextTestRunner(verbosity=2).run(TSOLAR)
    #unittest.TextTestRunner(verbosity=2).run(AESOLAR)
    unittest.TextTestRunner(verbosity=2).run(UTIL)
    #unittest.TextTestRunner(verbosity=2).run(INSOLAR)

#end if
