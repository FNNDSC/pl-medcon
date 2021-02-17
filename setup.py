from os import path
from setuptools import setup

with open(path.join(path.dirname(path.abspath(__file__)), 'README.rst')) as f:
    readme = f.read()

setup(
    name             = 'medcon',
    version          = '1.0.4',
    description      = 'An app to convert NIfTI volumes to DICOM files',
    long_description = readme,
    author           = 'Arushi Vyas',
    author_email     = 'dev@babyMRI.org',
    url              = 'https://github.com/FNNDSC/pl-medcon',
    packages         = ['medcon'],
    install_requires = ['chrisapp', 'nose', 'pudb'],
    test_suite       = 'nose.collector',
    tests_require    = ['nose'],
    license          = 'MIT',
    zip_safe         = False,
    python_requires  = '>=3.8',
    entry_points     = {
        'console_scripts': [
            'medcon = medcon.__main__:main'
            ]
        }
)
