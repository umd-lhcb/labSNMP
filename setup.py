#!/usr/bin/env python3

from setuptools import setup, find_packages
from os import path
from io import open

from labSNMP import name, version

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name=name,
    version=version,
    description='Python wrapper to control UMD LHCb group lab PSUs via SNMP protocol.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/umd-lhcb/labSNMP',

    author='UMD LHCb group',
    author_email='lhcb@physics.umd.edu',

    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 3',
    ],

    packages=find_packages(),

    python_requires='>=3, <4',
    install_requires=['pysnmp']
)
