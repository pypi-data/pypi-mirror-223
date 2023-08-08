import datetime
import re

import loguru

TimeType = datetime.datetime | None
CoordsType = tuple[float, float] | None

LOGGER = loguru.logger
FAILED_CACHE_SIZES = 65536

MIN_LOCATION_TIME = datetime.datetime(1960, 1, 1)
MAX_LOCATION_TIMEDELTA = datetime.timedelta(days=10)

TIME_PATTERN = re.compile(r'\d{2}:\d{2}:\d{2}$')
DATETIME_PATTENS = {
    re.compile(r'^\d{4}:\d{2}:\d{2} \d{2}:\d{2}:\d{2}$'): '%Y:%m:%d %H:%M:%S',
    re.compile(r'^\d{4}:\d{2}:\d{2}$'): '%Y:%m:%d',
    re.compile(r'^\d{4}:\d{2}:\d{2} \d{2}:\d{2}:\d{2}[-+]\d{2}:\d{2}$'): '%Y:%m:%d %H:%M:%S%z',
    re.compile(r'^\d{4}/\d{2}/\d{2} \d{2}:\d{2}:\d{2}$'): '%Y/%m/%d %H:%M:%S',
    re.compile(r'^\d{4}/\d{2}/\d{2}$'): '%Y/%m/%d',
    re.compile(r'^\d{2}/\d{2}/\d{4}$'): '%d/%m/%Y',
    re.compile(r'^\d{2}/\d{2}/\d{4} \d{1,2}:\d{2}$'): '%d/%m/%Y %H:%M',
    re.compile(r'^\d{2}/\d{2}/\d{4} \d{2}:\d{2}:\d{2}$'): '%d/%m/%Y %H:%M:%S',
    re.compile(r'^\d{1,2} .{3} \d{4} \d{2}:\d{2}:\d{2}$'): '%d %b %Y %H:%M:%S',
    re.compile(r'^\d{1,2} .{3} \d{4}$'): '%d %b %Y',
}
