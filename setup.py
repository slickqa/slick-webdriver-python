#!vpy/bin/python

__author__ = 'Jason Corbett'

from setuptools import setup, find_packages

import sys

requirements = []
with open('requirements.txt', 'r') as reqfile:
    requirements.extend(reqfile.read().split())

# get the backport of the enum module if python version is less than 3.4
if sys.version_info[0] < 3 or sys.version_info[1] < 4:
    requirements.append('enum34')

build_requirements = []
with open('build-requirements.txt', 'r') as reqfile:
    build_requirements.extend(reqfile.read().split())

setup(
    name="slick-webdriver",
    description="A webdriver wrapper api for the slickqa project (and anyone else who wants it).",
    version="1.0" + open("build.txt").read(),
    keywords="selenium webdriver testing qa web unittest nose",
    long_description=open('README.rst').read(),
    py_modules=['slickwd',],
    package_data={'': ['*.txt', '*.rst', '*.html']},
    include_package_data=True,
    install_requires=requirements,
    setup_requires=build_requirements,
    author="SlickQA Developers",
    url="http://www.slickqa.com/webdriver/python"
)
