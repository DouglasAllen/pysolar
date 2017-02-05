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
This file is consists of numerical constants for calculating corrections,
such as the wiggling ("nutation") of the axis of the earth. It also includes
functions for building dictionaries of polynomial functions for rapid
calculation of corrections.

Most of the constants come from a 2005 paper by Reda and Andreas:

I. Reda and A. Andreas, "Solar Position Algorithm for Solar Radiation
Applications," National Renewable Energy Laboratory, NREL/TP-560-34302,
revised November 2005.

http://www.osti.gov/bridge/servlets/purl/15003974-iP3z6k/native/15003974.PDF

However, it seems that Reda and Andreas took the bulk of the constants
(L0, etc.) from Pierre Bretagnon and Gerard Francou's Variations Seculaires
des Orbites Planetaires, or VSOP87:

http://en.wikipedia.org/wiki/Secular_variations_of_the_planetary_orbits#VSOP87

See also ftp://ftp.imcce.fr/pub/ephem/planets/vsop87/VSOP87D.ear
"""

# ABERRATION_COEFFS = None

def aberration_coeffs(nutation_coeffs=None):
    """
    This function builds a dictionary of polynomial functions from a list of
    coefficients, so that the functions can be called by name. This is used in
    calculating nutation.
    see: http://aa.usno.navy.mil/publications/docs/Circular_179.pdf
    """

    # global ABERRATION_COEFFS
    if nutation_coeffs is None:
        nutation_coeffs = dict \
          (
              (name, (
                  lambda a, b, c, d, e:
                  lambda x: (((e * x + d) * x + c) * x + b) * x + a)(*coeffs))
              for name, coeffs in
              (
                  ('MeanAnomalyOfMoon',
                   (134.96340251, 477198.8675605, 0.008855333, 1.43430556e-05, -6.797222e-08)),
                  ('MeanAnomalyOfSun',
                   (357.52911, 35999.05029, -0.0001537, 3.778e-08, -3.191667e-09)),
                  ('ArgumentOfLatitudeOfMoon',
                   (93.272091, 483202.0174577, -0.003542, -2.880555e-07, 1.158333e-09)),
                  ('MeanElongationOfMoon',
                   (297.8501955, 445267.1114469445, -0.0017696, 1.831389e-06, 8.802778e-09)),
                  ('LongitudeOfAscendingNode',
                   (125.044555, -1934.136262, 0.0020756, 2.139444e-06, 1.649722e-08))
              )
          )
    #end if
    return nutation_coeffs
#end get_aberration_coeffs

EARTH_RADIUS = 6378140.0 # meters
EARTH_AXIS_INCLINATION = 23.45 # degrees
SECONDS_PER_DAY = 86400

STANDARD_PRESSURE = 101325.00 # pascals
STANDARD_TEMPERATURE = 288.15 # kelvin
CELSIUS_OFFSET = 273.15 # subtract from kelvin to get deg C, add to deg C to get kelvin
EARTH_TEMPERATURE_LAPSE_RATE = -0.0065 # change in temperature with height, kelvin/metre
AIR_GAS_CONSTANT = 8.31432 # N*m/s^2
EARTH_GRAVITY = 9.80665 # m/s^2 or N/kg
EARTH_ATMOSPHERE_MOLAR_MASS = 0.0289644 # kg/mol

# Fundamental Argument Multipliers
FAM = \
    [
        [0, 0, 0, 0, 1],
        [0, 0, 2, -2, 2],
        [0, 0, 2, 0, 2],
        [0, 0, 0, 0, 2],
        [0, 1, 0, 0, 0],
        [0, 1, 2, -2, 2],
        [1, 0, 0, 0, 0],
        [0, 0, 2, 0, 1],
        [1, 0, 2, 0, 2],
        [0, -1, 2, -2, 2],
        [0, 0, 2, -2, 1],
        [-1, 0, 2, 0, 2],
        [-1, 0, 0, 2, 0],
        [1, 0, 0, 0, 1],
        [-1, 0, 0, 0, 1],
        [-1, 0, 2, 2, 2],
        [1, 0, 2, 0, 1],
        [-2, 0, 2, 0, 1],
        [0, 0, 0, 2, 0],
        [0, 0, 2, 2, 2],
        [0, -2, 2, -2, 2],
        [-2, 0, 0, 2, 0],
        [2, 0, 2, 0, 2],
        [1, 0, 2, -2, 2],
        [-1, 0, 2, 0, 1],
        [2, 0, 0, 0, 0],
        [0, 0, 2, 0, 0],
        [0, 1, 0, 0, 1],
        [-1, 0, 0, 2, 1],
        [0, 2, 2, -2, 2],
        [0, 0, -2, 2, 0],
        [1, 0, 0, -2, 1],
        [0, -1, 0, 0, 1],
        [-1, 0, 2, 2, 1],
        [0, 2, 0, 0, 0],
        [1, 0, 2, 2, 2],
        [-2, 0, 2, 0, 0],
        [0, 1, 2, 0, 2],
        [0, 0, 2, 2, 1],
        [0, -1, 2, 0, 2],
        [0, 0, 0, 2, 1],
        [1, 0, 2, -2, 1],
        [2, 0, 2, -2, 2],
        [-2, 0, 0, 2, 1],
        [2, 0, 2, 0, 1],
        [0, -1, 2, -2, 1],
        [0, 0, 0, -2, 1],
        [-1, -1, 0, 2, 0],
        [2, 0, 0, -2, 1],
        [1, 0, 0, 2, 0],
        [0, 1, 2, -2, 1],
        [1, -1, 0, 0, 0],
        [-2, 0, 2, 0, 2],
        [3, 0, 2, 0, 2],
        [0, -1, 0, 2, 0],
        [1, -1, 2, 0, 2],
        [0, 0, 0, 1, 0],
        [-1, -1, 2, 2, 2],
        [-1, 0, 2, 0, 0],
        [0, -1, 2, 2, 2],
        [-2, 0, 0, 0, 1],
        [1, 1, 2, 0, 2],
        [2, 0, 0, 0, 1],
        [-1, 1, 0, 1, 0],
        [1, 1, 0, 0, 0],
        [1, 0, 2, 0, 0],
        [-1, 0, 2, -2, 1],
        [1, 0, 0, 0, 2]
    ]

NUTATION_COEFFICIENTS = \
    [
        [-171996, -174.2, 92025, 8.9],
        [-13187, -1.6, 5736, -3.1],
        [-2274, -0.2, 977, -0.5],
        [2062, 0.2, -895, 0.5],
        [1426, -3.4, 54, -0.1],
        [712, 0.1, -7, 0],
        [-517, 1.2, 224, -0.6],
        [-386, -0.4, 200, 0],
        [-301, 0, 129, -0.1],
        [217, -0.5, -95, 0.3],
        [-158, 0, 0, 0],
        [129, 0.1, -70, 0],
        [123, 0, -53, 0],
        [63, 0, 0, 0],
        [63, 0.1, -33, 0],
        [-59, 0, 26, 0],
        [-58, -0.1, 32, 0],
        [-51, 0, 27, 0],
        [48, 0, 0, 0],
        [46, 0, -24, 0],
        [-38, 0, 16, 0],
        [-31, 0, 13, 0],
        [29, 0, 0, 0],
        [29, 0, -12, 0],
        [26, 0, 0, 0],
        [-22, 0, 0, 0],
        [21, 0, -10, 0],
        [17, -0.1, 0, 0],
        [16, 0, -8, 0],
        [-16, 0.1, 7, 0],
        [-15, 0, 9, 0],
        [-13, 0, 7, 0],
        [-12, 0, 6, 0],
        [11, 0, 0, 0],
        [-10, 0, 5, 0],
        [-8, 0, 3, 0],
        [7, 0, -3, 0],
        [-7, 0, 0, 0],
        [-7, 0, 3, 0],
        [-7, 0, 3, 0],
        [6, 0, 0, 0],
        [6, 0, -3, 0],
        [6, 0, -3, 0],
        [-6, 0, 3, 0],
        [-6, 0, 3, 0],
        [5, 0, 0, 0],
        [-5, 0, 3, 0],
        [-5, 0, 3, 0],
        [-5, 0, 3, 0],
        [4, 0, 0, 0],
        [4, 0, 0, 0],
        [4, 0, 0, 0],
        [-4, 0, 0, 0],
        [-4, 0, 0, 0],
        [-4, 0, 0, 0],
        [3, 0, 0, 0],
        [-3, 0, 0, 0],
        [-3, 0, 0, 0],
        [-3, 0, 0, 0],
        [-3, 0, 0, 0],
        [-3, 0, 0, 0],
        [-3, 0, 0, 0],
        [-3, 0, 0, 0],
    ]

"""
# L
HELIOCENTRIC_LONGITUDE_COEFFS = \
(
    (
        (1.75347046, 0.0000000, 0.00000000),
    ),
    (
        (6283.31966747, 0.00000000000, 0.00000000000),
    ),
    (
        (0.00052919, 0.00000000000, 0.00000000000),
    ),
    (
        (0.00000289, 5.844, 6283.076),
    ),
    (
        (0.00000114, 3.142, 0.000),
    ),
    (
        (0.00000001, 3.142, 0.000),
    ),
)
"""
# L
HELIOCENTRIC_LONGITUDE_COEFFS = \
(
    (# L0 70 of 559
        (1.75347046, 0.0000000, 0.00000000), # 1
        (0.03341656, 4.6692568, 6283.07585), # 2
        (0.00034894, 4.6261000, 12566.1517), # 3
        (0.00003497, 2.7441000, 5753.38490), # 5
        (0.00003418, 2.8289000, 3.52310000), # 4
        (0.00003136, 3.6280000, 77713.7715), # 6
        (0.00002676, 4.4181000, 7860.41940), # 7
        (0.00002343, 6.1352000, 3930.20970), # 8
        (0.00001273, 2.0371000, 529.691000), # 9
        (0.00001324, 0.7425000, 11506.7698), # 10

        (0.00000902, 2.0450000, 26.2980000), # 11
        (0.00001199, 1.1096000, 1577.34350), # 12
        (0.00000857, 3.5080000, 398.149000), # 13
        (0.00000780, 1.1790000, 5223.69400), # 14
        (0.00000990, 5.2330000, 5884.92700), # 15
        (0.00000753, 2.5330000, 5507.55300), # 16
        (0.00000505, 4.5830000, 18849.2280), # 17
        (0.00000492, 4.2050000, 775.523000), # 18
        (0.00000357, 2.9200000, 0.06700000), # 19
        (0.00000284, 1.8990000, 796.298000), # 20


        (0.00000243, 0.3450000, 5486.77800), # 21
        (0.00000317, 5.8490000, 11790.6290), # 22
        (0.00000271, 0.3150000, 10977.0790), # 23
        (0.00000206, 4.8060000, 2544.31400), # 24
        (0.00000205, 1.8690000, 5573.14300), # 25
        (0.00000202, 2.4580000, 6069.77700), # 26
        (0.00000126, 1.0830000, 20.7750000), # 27
        (0.00000156, 0.8330000, 213.299000), # 28
        (0.00000115, 0.6450000, 0.98000000), # 29
        (0.00000103, 0.6360000, 4694.00300), # 30

        (0.00000102, 4.2670000, 7.11400000), # 31
        (0.00000099, 6.2100000, 2146.17000), # 32
        (0.00000132, 3.4110000, 2942.46300), # 33
        (0.00000098, 0.6800000, 155.420000), # 34
        (0.00000085, 1.3000000, 6275.96000), # 35
        (0.00000075, 1.7600000, 5088.63000), # 36
        (0.00000102, 0.9760000, 15720.8390), # 37
        (0.00000085, 3.6700000, 71430.7000), # 38
        (0.00000074, 4.6800000, 801.820000), # 39
        (0.00000074, 3.5000000, 3154.69000), # 40

        (0.00000079, 3.0400000, 12036.4600), # 41
        (0.00000080, 1.8100000, 17260.1500), # 42
        (0.00000086, 5.9800000, 161000.690), # 43
        (0.00000057, 2.7800000, 6286.60000), # 44
        (0.00000061, 1.8200000, 7084.90000), # 45
        (0.00000070, 0.8300000, 9437.76000), # 46
        (0.00000056, 4.3900000, 14143.5000), # 47
        (0.00000062, 3.9800000, 8827.39000), # 48
        (0.00000051, 0.2800000, 5856.48000), # 49
        (0.00000056, 3.4700000, 6279.55000), # 50

        (0.00000041, 5.3700000, 8429.24000), # 51
        (0.00000052, 1.3300000, 1748.02000), # 52
        (0.00000052, 0.1900000, 12139.5500), # 53
        (0.00000049, 0.4900000, 1194.45000), # 54
        (0.00000039, 6.1700000, 10447.3900), # 55
        (0.00000036, 1.7800000, 6812.77000), # 56
        (0.00000037, 6.0400000, 10213.2900), # 57
        (0.00000037, 2.5700000, 1059.38000), # 58
        (0.00000033, 0.5900000, 17789.8500), # 59
        (0.00000036, 1.7100000, 2352.87000), # 60

        (0.00000041, 2.4000000, 19651.0500), # 61
        (0.00000030, 2.7400000, 1349.87000), # 62
        (0.00000030, 0.4400000, 83996.8500), # 63
        # (0.00000024, 0.4850000, 8031.09000), # 64
        # (0.00000024, 2.0650000, 3340.60000), # 65
        # (0.00000021, 4.1480000, 951.720000), # 66
        # (0.00000025, 0.2150000, 3.59000000), # 67
        (0.00000025, 3.1600000, 4690.48000), # 68
        # (0.00000023, 5.2220000, 4705.73000), # 69
        # (0.00000021, 1.4260000, 16730.4600), # 70

        # (0.00000022, 5.5560000, 553.569000), # 71
        # (0.00000017, 4.5610000, 135.065080), # 72
        # (0.00000020, 5.2220000, 12168.0027), # 73
        # (0.00000020, 5.7750000, 6309.37417), # 74
        # (0.00000020, 0.3710000, 283.859319), # 75

    ), #
    # L1 34 of 341
    (
        (6283.31966747, 0.000000, 0.00000000), # 1
        (0.00206059000, 2.678000, 6283.07585), # 2
        (0.00004303000, 2.635100, 12566.1517), # 3
        (0.00000425000, 1.590000, 3.52300000), # 4
        (0.00000119000, 5.796000, 26.2980000), # 7
        (0.00000109000, 2.966000, 1577.34400), # 5
        (0.00000093000, 2.590000, 18849.2300), # 6
        (0.00000072000, 1.140000, 529.690000), # 8
        (0.00000068000, 1.870000, 398.150000), # 9
        (0.00000067000, 4.410000, 5507.55000), # 10

        (0.00000059000, 2.890000, 5223.69000), # 11
        (0.00000056000, 2.170000, 155.420000), # 12
        (0.00000045000, 0.400000, 796.300000), # 13
        (0.00000036000, 0.470000, 775.520000), # 14
        (0.00000029000, 2.650000, 7.11000000), # 15
        (0.00000019000, 1.850000, 5486.78000), # 16
        (0.00000021000, 5.340000, 0.98000000), # 17
        (0.00000019000, 4.970000, 213.300000), # 18
        (0.00000016000, 0.030000, 2544.31000), # 19
        (0.00000017000, 2.990000, 6275.96000), # 20

        (0.00000016000, 1.430000, 2146.17000), # 21
        (0.00000015000, 1.210000, 10977.0800), # 22
        (0.00000012000, 3.260000, 5088.63000), # 23
        (0.00000012000, 2.080000, 4694.00300), # 24
        (0.00000010000, 4.240000, 1349.87000), # 25
        (0.00000010000, 1.300000, 6286.60000), # 26
        (0.00000009000, 2.700000, 242.730000), # 27
        (0.00000012000, 2.830000, 1748.02000), # 28
        (0.00000012000, 5.270000, 1194.45000), # 29
        (0.00000009000, 5.640000, 951.720000), # 30

        (0.00000011000, 0.770000, 553.570000), # 31
        (0.00000008000, 5.300000, 2352.87000), # 32
        # (0.00000006000, 1.770000, 1059.38000), # 33
        (0.00000006000, 2.650000, 9437.76000), # 34
        # (0.00000005000, 5.670000, 71430.7000), # 35
        (0.00000006000, 4.670000, 4690.48000), # 37



    ),
    # L2 20 of 142
    (
        (0.00052919, 0.0000, 0.0000000), # 1
        (0.00008720, 1.0721, 6283.0758), # 2
        (0.00000309, 0.8670, 12566.152), # 3
        (0.00000027, 0.0500, 3.5200000), # 4
        (0.00000016, 5.1900, 26.300000), # 5
        (0.00000016, 3.6800, 155.42000), # 6
        (0.00000010, 0.7600, 18849.230), # 7
        (0.00000009, 2.0600, 77713.770), # 8
        (0.00000007, 0.8300, 775.52000), # 9
        (0.00000005, 4.6600, 1577.3400), # 10

        (0.00000004, 1.0300, 7.1100000), # 11
        (0.00000004, 3.4400, 5573.1400), # 16
        (0.00000003, 5.1400, 796.30000), # 12
        (0.00000003, 6.0500, 5507.5500), # 13
        (0.00000003, 1.1900, 242.73000), # 14
        (0.00000003, 6.1200, 529.69000), # 15
        (0.00000003, 0.3100, 398.15000), # 17
        (0.00000003, 2.2800, 553.57000), # 19
        (0.00000002, 4.3800, 5223.6900), # 18
        (0.00000002, 3.7500, 0.9800000), # 20
    ),
    # L3 10 of 22
    (
        (0.0000028900, 5.844, 6283.076), # 1
        (0.0000003500, 0.000, 0.000000), # 2
        (0.0000001700, 5.488, 12566.15), # 3
        (0.0000000300, 5.200, 155.4200), # 4
        (0.0000000100, 4.720, 3.520000), # 5
        (0.0000000100, 5.970, 242.7300), # 6
        (0.0000000100, 5.300, 18849.23), # 7
        # (0.0000000040, 3.787, 553.5694), # 8
        # (0.0000000007, 4.298, 6286.599), # 9
        # (0.0000000007, 0.907, 6127.655), # 10
        # (0.0000000004, 5.240, 6438.496), # 11
    ),
    # L4 all 11
    (
        (0.00000114000, 3.142, 0.000000), # 1
        (0.00000008000, 4.134, 6283.080), # 2
        (0.00000001000, 3.840, 12566.15), # 3
        # (0.00000000400, 0.420, 155.4000), # 4
        # (0.00000000040, 3.600, 18849.23), # 5
        # (0.00000000040, 3.141, 3.500000), # 6
        # (0.00000000030, 5.003, 5573.143), # 7
        # (0.00000000010, 0.488, 77713.77), # 8
        # (0.00000000010, 5.648, 6127.655), # 9
        # (0.00000000010, 2.842, 161000.7), # 10
        # (0.00000000002, 0.549, 6438.500), # 11
    ),
    # L5 all 5
    (
        (0.00000001000, 3.14, 0.000000), # 1
        # (0.00000000200, 2.77, 6283.100), # 2
        # (0.00000000050, 2.00, 155.4000), # 3
        # (0.00000000030, 2.21, 12566.15), # 4
        # (0.00000000005, 1.76, 18849.23), # 5
    ),
)

# B
HELIOCENTRIC_LATITUDE_COEFFS = \
(
    ( # B0 5 of 184
        (0.00000280, 3.199, 84334.662), # 1
        (0.00000102, 5.422, 5507.5530), # 2
        (0.00000080, 3.880, 5223.6939), # 3
        (0.00000044, 3.704, 2352.8662), # 4
        (0.00000032, 4.000, 1577.3435), # 5
    ),
    ( # B1 3 of 99
        (0.00000009, 3.897, 5507.5532), # 1
        (0.00000006, 1.730, 5223.6939), # 2
        # (0.00000004, 5.244, 2352.8662), # 3
    ),
    ( # B2 2 of 49
        # (0.00000002, 1.627, 84334.6616), # 1
        # (0.00000001, 2.414, 1047.7473), # 2
    ),
    ( # B3 1 of 11
        # (0.00000000011, 0.23877262399, 7860.41939243920), # 1
    ),
    ( # B4 1 of 5
        # (0.00000000004, 0.79662198849, 6438.49624942560), # 1
    ),
)

# R
AU_DISTANCE_COEFFS = \
(
    ( #R0
        (100013989.0, 0.0, 0.0),
        (1670700.0, 3.0984635, 6283.07585),
        (13956.0, 3.05525, 12566.1517),
        (3084.0, 5.1985, 77713.7715),
        (1628.0, 1.1739, 5753.3849),
        (1576.0, 2.8469, 7860.4194),
        (925.0, 5.453, 11506.77),
        (542.0, 4.564, 3930.21),
        (472.0, 3.661, 5884.927),
        (346.0, 0.964, 5507.553),
        (329.0, 5.9, 5223.694),
        (307.0, 0.299, 5573.143),
        (243.0, 4.273, 11790.629),
        (212.0, 5.847, 1577.344),
        (186.0, 5.022, 10977.079),
        (175.0, 3.012, 18849.228),
        (110.0, 5.055, 5486.778),
        (98.0, 0.89, 6069.78),
        (86.0, 5.69, 15720.84),
        (86.0, 1.27, 161000.69),
        (65.0, 0.27, 17260.15),
        (63.0, 0.92, 529.69),
        (57.0, 2.01, 83996.85),
        (56.0, 5.24, 71430.7),
        (49.0, 3.25, 2544.31),
        (47.0, 2.58, 775.52),
        (45.0, 5.54, 9437.76),
        (43.0, 6.01, 6275.96),
        (39.0, 5.36, 4694.0),
        (38.0, 2.39, 8827.39),
        (37.0, 0.83, 19651.05),
        (37.0, 4.9, 12139.55),
        (36.0, 1.67, 12036.46),
        (35.0, 1.84, 2942.46),
        (33.0, 0.24, 7084.9),
        (32.0, 0.18, 5088.63),
        (32.0, 1.78, 398.15),
        (28.0, 1.21, 6286.6),
        (28.0, 1.9, 6279.55),
        (26.0, 4.59, 10447.39),
    ),
    ( # R1
        (103019.0, 1.10749, 6283.07585),
        (1721.0, 1.0644, 12566.1517),
        (702.0, 3.142, 0.0),
        (32.0, 1.02, 18849.23),
        (31.0, 2.84, 5507.55),
        (25.0, 1.32, 5223.69),
        (18.0, 1.42, 1577.34),
        (10.0, 5.91, 10977.08),
        (9.0, 1.42, 6275.96),
        (9.0, 0.27, 5486.78),
    ),
    ( # R2
        (4359.0, 5.7846, 6283.0758),
        (124.0, 5.579, 12566.152),
        (12.0, 3.14, 0.0),
        (9.0, 3.63, 77713.77),
        (6.0, 1.87, 5573.14),
        (3.0, 5.47, 18849.23),
    ),
    ( # R3
        (145.0, 4.273, 6283.076),
        (7.0, 3.92, 12566.15),
    ),
    ( # R4
        (4.0, 2.56, 6283.08),
    ),
)
