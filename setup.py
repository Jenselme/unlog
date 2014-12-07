#!/usr/bin/python3
# -*- coding: utf-8 -*-
from setuptools import setup
from setuptools.command.test import test as TestCommand

class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        # import here, cause outside the eggs aren't loaded
        import pytest
        pytest.main(self.test_args)

setup(
    name = "unlog",
    version = "1.0.0",
    packages = ['unlog'],
    requires=['sh'],
    tests_require=['pytest'],
    cmdclass = {'test': PyTest},
    author = "Julien Enselme",
    author_email = "jenselme@jujens.eu",
    description = "Python script to easy unloging.",
    license = "MIT",
    keywords="log",
    url = "https://bitbucket.org/Jenselme/dcvsapi",
    classifiers="""Development Status :: 5 - Production/Stable
Intended Audience :: Developers
License :: OSI Approved :: BSD License
Operating System :: OS Independent
Programming Language :: Python :: 3
Programming Language :: Python :: 3.2
Programming Language :: Python :: 3.3
Programming Language :: Python :: 3.4
Topic :: System :: Logging""".split('\n'),
    long_description="""Python script to ease the unloging of file when we need
    to get line in the file from a starting line to an end line.
""",
    entry_points={
    'console_scripts': [
      'unlog = unlog.main:main',
    ],
  },
)
