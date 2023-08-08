import re

from setuptools import setup, find_packages

REPO_NAME = 'image2gps'
PACKAGE_NAME = REPO_NAME.lower()
URL = f'https://github.com/abionics/{REPO_NAME}'


def get_version() -> str:
    code = read_file(f'{PACKAGE_NAME}/__init__.py')
    return re.search(r'__version__ = \'(.+?)\'', code).group(1)


def load_readme() -> str:
    return read_file('README.md')


def read_file(filename: str) -> str:
    with open(filename) as file:
        return file.read()


setup(
    name=PACKAGE_NAME,
    version=get_version(),
    description='Extract time and coords from image 🖼📍⏱️',
    long_description=load_readme(),
    long_description_content_type='text/markdown',
    author='Alex Ermolaev',
    author_email='abionics.dev@gmail.com',
    url=URL,
    license='MIT',
    keywords='image gps location extract exif',
    install_requires=[
        'loguru',
        'pillow',
        'piexif',
        'cachetools',
    ],
    classifiers=[
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Topic :: Scientific/Engineering :: GIS',
        'Topic :: Scientific/Engineering :: Image Processing',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Typing :: Typed',
    ],
    packages=find_packages(exclude=['tests']),
    zip_safe=False,
)
