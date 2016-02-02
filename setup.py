#-*-encoding: utf-8-*-
from __future__ import unicode_literals

import re

from setuptools import find_packages, setup


def get_version(filename):
    with open(filename) as fh:
        metadata = dict(re.findall("__([a-z]+)__ = '([^']+)'", fh.read()))
        return metadata['version']


setup(
    name='MopidyCLI',
    version=get_version('mopidycli/__init__.py'),
    url='https://github.com/havardgulldahl/mopidycli',
    license='Apache License, Version 2.0',
    author='Håvard Gulldahl',
    author_email='havard@gulldahl.no',
    description='Mopidy tool controlling playback from command line',
    long_description=open('README.rst').read(),
    packages=find_packages(exclude=['tests', 'tests.*']),
    zip_safe=False,
    include_package_data=True,
    install_requires=[
        'setuptools',
        'jsonrpclib',
    ],
    entry_points={
        'console_scripts': [
            'mopidy-state = mopidycli.cli:state',
            'mopidy-play = mopidycli.cli:play',
            'mopidy-pause = mopidycli.cli:pause',
            'mopidy-resume = mopidycli.cli:resume',
            'mopidy-next = mopidycli.cli:next',
            'mopidy-previous = mopidycli.cli:previous',
            'mopidy-tracklist = mopidycli.cli:tracklist',
            'mopidy-shuffle = mopidycli.cli:shuffle',
        ],
    },
    classifiers=[
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Topic :: Multimedia :: Sound/Audio :: Players',
    ],
)
