
# Core Python imports.
import math

# Local imports.
from . import utils

#wgs84_earth_equatorial_radius_m = 6378137
wgs84_earth_equatorial_radius_m = 6371000

def BearingBetween(lat_1, lon_1, lat_2, lon_2, degrees=True):
    """ Calculate initial bearing between two locations.

    From: https://www.movable-type.co.uk/scripts/latlong.html
    """
    if degrees:
        lat_1 = utils.DegToRad(lat_1)
        lon_1 = utils.DegToRad(lon_1)
        lat_2 = utils.DegToRad(lat_2)
        lon_2 = utils.DegToRad(lon_2)

    delta_lon = lon_2 - lon_1

    brg = math.atan2(
        math.sin(delta_lon) * math.cos(lat_2),
        (math.cos(lat_1) * math.sin(lat_2)) - 
            (math.sin(lat_1) * math.cos(lat_2) * math.cos(delta_lon))
    )

    return utils.RadToDeg(brg)

def DistanceBetween(lat_1, lon_1, lat_2, lon_2, degrees=True):
    """ Calculate distance between two location in metres.

    From: https://www.movable-type.co.uk/scripts/latlong.html
    """
    global wgs84_earth_equatorial_radius_m
    
    if degrees:
        lat_1 = utils.DegToRad(lat_1)
        lon_1 = utils.DegToRad(lon_1)
        lat_2 = utils.DegToRad(lat_2)
        lon_2 = utils.DegToRad(lon_2)
        
    delta_lat = lat_2 - lat_1
    delta_lon = lon_2 - lon_1
    
    a = (math.sin(delta_lat / 2) * math.sin(delta_lat / 2)) + (math.cos(lat_1) * math.cos(lat_2) * math.sin(delta_lon / 2) * math.sin(delta_lon / 2))
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    d = wgs84_earth_equatorial_radius_m * c
    return d

def Extrapolate(lat, lon, brg, dst, degrees=True):
    """ Calculate a new position given a start position, bearing and distance

    Given an initial latitude and longitude, calculate a new latitude and
    longitude by extrapolating from the start point along the bearing 'brg'
    for a distance specified by 'dst'.

    It is assumed that all angles (lat, lon, brg) are in degrees. If not, set
    'degrees' to False.

    The units of 'dst' is metres.
    
    From: https://www.movable-type.co.uk/scripts/latlong.html
    """
    # Calculate angular distance.
    global wgs84_earth_equatorial_radius_m
    ang_dst = dst / wgs84_earth_equatorial_radius_m

    # If angles are in degrees, convert to radians to do our maths.
    if degrees:
        lat = utils.DegToRad(lat)
        lon = utils.DegToRad(lon)
        brg = utils.DegToRad(brg)

    tlat = math.asin(
        (math.sin(lat) * math.cos(ang_dst)) + (math.cos(lat) * math.sin(ang_dst) * math.cos(brg))
    )
    tlon = lon + math.atan2(
        math.sin(brg) * math.sin(ang_dst) * math.cos(lat),
        math.cos(ang_dst) - (math.sin(lat) * math.sin(tlat))
    )
    return utils.RadToDeg(tlat), utils.RadToDeg(tlon)