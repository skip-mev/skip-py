import os
from setuptools import setup

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "skip-py",
    version = "0.1.2",
    author = "Jeremy Liu",
    author_email = "jeremy@skip.money",
    description = ("A helper library to sign and send bundles to the Skip Relay in Python."),
    license = "MIT",
    url = "http://packages.python.org/an_example_pypi_project",
    packages=['skip'],
    requires=["setuptools>=61.0", "cosmpy>=0.6.0", "httpx>=0.23.0"],
    long_description=read('README'),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)