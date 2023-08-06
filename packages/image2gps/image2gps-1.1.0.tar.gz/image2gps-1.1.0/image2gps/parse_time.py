import datetime

import piexif

from image2gps.config import LOGGER, MIN_LOCATION_TIME, MAX_LOCATION_TIMEDELTA, DATETIME_PATTENS, TimeType


# todo parse "2000:01:01 24:01:90", "24 Фев 2016 г."
def parse_time(exif: dict) -> TimeType:
    zero_th = exif.get('0th', {})
    time = zero_th.get(piexif.ImageIFD.DateTime)
    if time is None:
        return None
    try:
        time = time.replace(b'\x00', b'').strip().decode().removesuffix('Z')
        if len(time) == 0 or time.startswith('0000:00:00'):
            return None
        time = _string_to_datetime(time)
    except Exception as e:
        LOGGER.debug(f'Failed to parse time "{time}" due to {e} ({type(e)})')
        return None
    max_date = datetime.datetime.now() + MAX_LOCATION_TIMEDELTA
    if time < MIN_LOCATION_TIME or time > max_date:
        LOGGER.debug(f'Date "{time}" is out of range')
        return None
    return time


def _string_to_datetime(value: str) -> datetime.datetime:
    for pattern, timelike in DATETIME_PATTENS.items():
        if pattern.match(value):
            return datetime.datetime.strptime(value, timelike)
    return datetime.datetime.fromisoformat(value)
