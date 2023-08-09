#!/usr/bin/env python

import setuptools

setuptools.setup(name='zephyrcore',
                 version='2.0',
                 description='Python Distribution Utilities',
                 author='QM Core Team',
                 author_email='business.agility@ab-inbev.com',
                 long_description=open('README.md').read(),
                 long_description_content_type='text/markdown',
                 url='https://www.python.org/sigs/distutils-sig/',
                 packages=setuptools.find_packages(),
                 python_requires='>=3.9',
                 py_modules=["zephyrcore"],
                 install_requires=['requests', 'atlassian-python-api', 'json']  # Optional
                 )
