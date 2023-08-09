#!/usr/bin/env python

from distutils.core import setup

setup(name='zephyrcore',
      version='1.0',
      description='Python Distribution Utilities',
      author='QM Core Team',
      author_email='business.agility@ab-inbev.com',
      long_description=open('README.md').read(),
      long_description_content_type='text/markdown',
      url='https://www.python.org/sigs/distutils-sig/',
      packages=['core']
      )
