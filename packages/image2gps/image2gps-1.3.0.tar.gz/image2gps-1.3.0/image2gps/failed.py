from cachetools import LRUCache

from image2gps.config import LOGGER, FAILED_CACHE_SIZES

FAILED_CACHE = LRUCache(FAILED_CACHE_SIZES)


def on_fail(key: int, reason: str):
    if key in FAILED_CACHE:
        return
    FAILED_CACHE[key] = True
    LOGGER.debug(reason)
