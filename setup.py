from distutils.core import setup
from setuptools import setup, find_packages
setup(
    name="DARNprocessing",
    version="0.1dev",
    license="GNU",
    packages=find_packages(exclude=['docs', 'test']),
    author="SuperDARN Canada",
    scripts=['./bin/fitdata2convectionPlots.py','./bin/fitdata2map.py','./bin/omniDataAvailability']
)




