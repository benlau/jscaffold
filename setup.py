#!/usr/bin/env python
# coding: utf-8

from __future__ import print_function
from glob import glob
import os
from os.path import join as pjoin
from setuptools import setup
from jscaffold._version import __version__
HERE = os.path.dirname(os.path.abspath(__file__))

name = 'jscaffold'
version = __version__

setup_args = dict(
    name=name,
    description='Jupyter Scaffold',
    version=version,
    scripts=glob(pjoin('scripts', '*')),
    author='Ben lau',
    author_email='xbenlau@gmail.com',
    url='https://github.com/benlau/jscaffold',
    license='BSD',
    platforms="Linux, Mac OS X, Windows",
    keywords=['Jupyter', 'Widgets', 'IPython'],
    classifiers=[
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Framework :: Jupyter',
    ],
    include_package_data=True,
    python_requires=">=3.6",
    install_requires=[
        'ipywidgets>=7.0.0'
    ],
    extras_require={
        'test': [
            'pytest>=4.6',
            'pytest-cov',
            'nbval',
        ],
        'examples': [
            # Any requirements for the examples to run
        ],
        'docs': [
        ],
    },
    entry_points={
    },
)

if __name__ == '__main__':
    setup(**setup_args)
