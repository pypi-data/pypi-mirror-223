import piexif

from image2gps.config import LOGGER, CoordsType


def parse_coords(exif: dict) -> CoordsType:
    gps = exif.get('GPS')
    if gps is None or len(gps) == 0:
        return None
    lat = gps.get(piexif.GPSIFD.GPSLatitude)
    lon = gps.get(piexif.GPSIFD.GPSLongitude)
    if lat is None or lon is None:
        LOGGER.debug(f'Failed to parse GPS "{gps}"')
        return None
    lat, lon = _value_to_degrees(lat), _value_to_degrees(lon)
    if lat == 0 and lon == 0:
        return None
    return lat, lon


def _value_to_degrees(value: tuple) -> float:
    if value[0][1] == 0:
        return 0
    result = value[0][0] / value[0][1]
    if value[1][1] == 0:
        return result
    result += value[1][0] / value[1][1] / 60
    if value[2][1] == 0:
        return result
    return result + value[2][0] / value[2][1] / 3600
