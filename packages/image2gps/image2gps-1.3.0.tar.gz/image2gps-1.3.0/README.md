# image2gps

Extract time and coords from image 🖼📍⏱️

![demo](demo.jpg)
_[Image source](https://github.com/ianare/exif-samples/blb/master/jpg/gps/DSCN0010.jpg)_

```python
from image2gps import image2gps

time, coords = image2gps('demo.jpg')
print(f'Image taken in {coords} at {time}')
# >>> Image taken in (43.467, 11.885) at 2008-11-01 21:15:07
```

This sample can be found [here](tests/sample.py)


## Installation

```bash
pip install image2gps
```


## Tests

```bash
python -m pytest tests

# or only certain tests
python -m pytest tests/test_main.py
python -m pytest tests/test_time.py
```


## More

PyPI: https://pypi.org/project/image2gps

Repository: https://github.com/abionics/image2gps

Developer: Alex Ermolaev (Abionics)

Email: abionics.dev@gmail.com

License: MIT (see LICENSE.txt)
