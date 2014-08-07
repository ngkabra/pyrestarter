#!/usr/bin/env python
from setuptools import setup

setup(name='pyrestarter',
      version='0.1.dev5',
      description='A utility to monitor and auto-restart programs',
      author='Navin Kabra',
      author_email='navin@smriti.com',
      url='https://github.com/ngkabra/pyrestarter',
      py_modules=['pyrestarter'],
      install_requires=['psutil'],
      )
