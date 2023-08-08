import datetime

import piexif

from image2gps.config import (
    TimeType,
    LOGGER,
    MIN_LOCATION_TIME,
    MAX_LOCATION_TIMEDELTA,
    TIME_PATTERN,
    DATETIME_PATTENS,
)


def parse_time(exif: dict) -> TimeType:
    zero_th = exif.get('0th', {})
    time = zero_th.get(piexif.ImageIFD.DateTime)
    if time is None:
        return None
    try:
        time = time.replace(b'\x00', b'').strip().decode().removesuffix('Z').removesuffix(' г.')
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
    value = _fix_time_overflow(value)
    for pattern, timelike in DATETIME_PATTENS.items():
        if pattern.match(value):
            return datetime.datetime.strptime(value, timelike).replace(tzinfo=None)
    return datetime.datetime.fromisoformat(value).replace(tzinfo=None)


def _fix_time_overflow(value: str) -> str:
    time = TIME_PATTERN.search(value)
    if time is None:
        return value
    time = time.group()
    hours, minutes, seconds = map(int, time.split(':'))
    if hours in range(24) and minutes in range(60) and seconds in range(60):
        return value
    hour = hours % 24
    minutes = minutes % 60
    seconds = seconds % 60
    return _replace_rightmost(value, time, f'{hour:02}:{minutes:02}:{seconds:02}')


def _replace_rightmost(value: str, old: str, new: str, count: int = 1) -> str:
    return new.join(value.rsplit(old, count))
