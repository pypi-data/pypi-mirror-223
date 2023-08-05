import math
def deg_to_rad(deg):
    return deg * (math.pi / 180.0)


def wgs84_to_turef_tm30(latitude, longitude):
    # TUREF TM30 projection parameters
    central_meridian = deg_to_rad(30.0)  # Meridian 30 degrees
    scale_factor = 1.0
    false_easting = 500000.0
    false_northing = 0.0

    # Convert latitude and longitude from degrees to radians
    lat_rad = deg_to_rad(latitude)
    lon_rad = deg_to_rad(longitude)

    # Constants for the TM30 projection
    a = 6378137.0  # Semi-major axis of WGS 84 ellipsoid in meters
    b = 6356752.314140356
    e2 = ((a ** 2) - (b ** 2)) / (a ** 2)

    # Calculate the parameters for the TM30 projection
    nu = a / math.sqrt(1 - e2 * math.sin(lat_rad) ** 2)
    rho = a * (1 - e2) / (1 - e2 * math.sin(lat_rad) ** 2) ** 1.5
    eta2 = nu / rho - 1

    A = (lon_rad - central_meridian) * math.cos(lat_rad)
    T = math.tan(lat_rad) ** 2
    C = e2 * math.cos(lat_rad) ** 2 / (1 - e2)

    M = a * ((1 - e2 / 4 - 3 * e2 ** 2 / 64 - 5 * e2 ** 3 / 256) * lat_rad -
             (3 * e2 / 8 + 3 * e2 ** 2 / 32 + 45 * e2 ** 3 / 1024) * math.sin(2 * lat_rad) +
             (15 * e2 ** 2 / 256 + 45 * e2 ** 3 / 1024) * math.sin(4 * lat_rad) -
             (35 * e2 ** 3 / 3072) * math.sin(6 * lat_rad))

    easting = false_easting + scale_factor * nu * (A + (1 - T + C) * A ** 3 / 6 +
                                                   (5 - 18 * T + T ** 2 + 72 * C - 58 * eta2) * A ** 5 / 120)
    northing = false_northing + scale_factor * (M + nu * math.tan(lat_rad) * (A ** 2 / 2 +
                                                                              (
                                                                                      5 - T + 9 * C + 4 * C ** 2) * A ** 4 / 24 +
                                                                              (
                                                                                      61 - 58 * T + T ** 2 + 600 * C - 330 * eta2) * A ** 6 / 720))

    return easting, northing
