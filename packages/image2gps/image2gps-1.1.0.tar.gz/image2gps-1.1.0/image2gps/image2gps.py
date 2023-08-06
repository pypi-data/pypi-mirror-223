from pathlib import Path

import piexif
from PIL import Image
from PIL.Image import Image as ImageType

from image2gps.config import TimeType, CoordsType
from image2gps.parse_coords import parse_coords
from image2gps.parse_time import parse_time


def image2gps(image: ImageType | Path | str, safe: bool = False) -> tuple[TimeType, CoordsType]:
    try:
        if not isinstance(image, ImageType):
            image = Image.open(image)
        exif = image.info.get('exif')
        exif = piexif.load(exif) if exif else dict()
        return parse_time(exif), parse_coords(exif)
    except Exception as e:
        if not safe:
            raise e
        return None, None
