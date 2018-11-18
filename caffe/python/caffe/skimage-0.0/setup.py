import sys

if not 'sdist' in sys.argv:
    sys.exit('\n*** Please install the `scikit-image` package '
            '(instead of `skimage`) ***\n')

from setuptools import setup

setup(
    name='skimage',
    version='0.0',
    description='Dummy package that points to scikit-image',
    url='https://github.com/scikit-image/scikit-image',
    author='Stefan van der Walt',
    author_email='stefanv@berkeley.edu'
)
