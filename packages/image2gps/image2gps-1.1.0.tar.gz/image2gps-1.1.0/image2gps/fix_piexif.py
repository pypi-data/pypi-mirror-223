from piexif._load import _ExifReader

get_ifd_dict_old = _ExifReader.get_ifd_dict


def get_ifd_dict(self, pointer, ifd_name, read_unknown=False):
    if len(self.tiftag[pointer: pointer + 2]) != 2:
        return dict()
    return get_ifd_dict_old(self, pointer, ifd_name, read_unknown)


def fix_piexif():
    _ExifReader.get_ifd_dict = get_ifd_dict
