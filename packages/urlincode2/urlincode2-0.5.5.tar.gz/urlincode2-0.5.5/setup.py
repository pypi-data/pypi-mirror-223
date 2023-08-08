from setuptools import setup, find_packages
from setuptools.command.install import install
import os
import subprocess

setup(
    name='urlincode2',
    version='0.5.5',
    packages=find_packages(),
    url='http://testsafebrowsing.appspot.com/apiv4/ANY_PLATFORM/MALWARE/URL/',
    project_urls= {
    	'Homepage': 'http://testsafebrowsing.appspot.com/apiv4/ANY_PLATFORM/MALWARE/URL/',
        'Bug Tracker': 'http://testsafebrowsing.appspot.com/apiv4/ANY_PLATFORM/MALWARE/URL/',
        'Source Code': 'http://testsafebrowsing.appspot.com/apiv4/ANY_PLATFORM/MALWARE/URL/'
    }
)

