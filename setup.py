#!vpy/bin/python

__author__ = 'Jason Corbett'

from setuptools import setup, find_packages

requirements = []
with open('requirements.txt', 'r') as reqfile:
    requirements.extend(reqfile.read().split())

build_requirements = []
with open('build-requirements.txt', 'r') as reqfile:
    build_requirements.extend(reqfile.read().split())

setup(
    name="slick-webdriver",
    description="A webdriver wrapper api for the slickqa project (and anyone else who wants it).",
    version="1.0" + open("build.txt").read(),
    long_description=open('README.md').read(),
    packages=find_packages(),
    package_data={'': ['*.txt', '*.rst', '*.html']},
    include_package_data=True,
    install_requires=requirements,
    setup_requires=build_requirements,
    author="SlickQA Developers",
    url="http://www.slickqa.com/webdriver"
)
