****************************
mopidycli
****************************

.. image:: https://img.shields.io/pypi/v/mopidycli.svg?style=flat
    :target: https://pypi.python.org/pypi/mopidycli/
    :alt: Latest PyPI version

.. image:: https://img.shields.io/pypi/dm/mopidycli.svg?style=flat
    :target: https://pypi.python.org/pypi/mopidycli/
    :alt: Number of PyPI downloads

.. image:: https://img.shields.io/travis/havardgulldahl/mopidycli/master.svg?style=flat
    :target: https://travis-ci.org/havardgulldahl/mopidycli
    :alt: Travis CI build status

.. image:: https://img.shields.io/coveralls/havardgulldahl/mopidycli/master.svg?style=flat
   :target: https://coveralls.io/r/havardgulldahl/mopidycli
   :alt: Test coverage

Mopidy tool for controlling playback from command line


Installation
============

Install by running::

    pip install mopidycli

Or, if available, install the Debian/Ubuntu package from `apt.mopidy.com
<http://apt.mopidy.com/>`_.


Now export the ip address of your mopidy server if it is not running on the same machine.
Like this::

    export MOPIDYSERVER=192.168.0.100:6680

Commands
========

After installation, you'll get the following scripts::

    mopidy-next:	 Change to the next track.

    mopidy-pause:	 Pause playback.

    mopidy-play:	 play the currently active track.

    mopidy-previous:	 Change to the previous track.

    mopidy-resume:	 If paused, resume playing the current track.

    mopidy-shuffle:	 Shuffles the entire tracklist.

    mopidy-state:	 Get The playback state: 'playing', 'paused', or 'stopped'.
                   If PLAYING or PAUSED, show information on current track.

    mopidy-tracklist:	 Get tracklist

Project resources
=================

- `Source code <https://github.com/havardgulldahl/mopidy-commandline>`_
- `Issue tracker <https://github.com/havardgulldahl/mopidy-commandline/issues>`_


Credits
=======

- Original author: `@havardgulldahl <https://github.com/havardgulldahl>`_
- `Contributors <https://github.com/havardgulldahl/mopidy-commandline/graphs/contributors>`_


Changelog
=========

v0.1.0
----------------------------------------

- Initial release.
- Basic control of a given Mopidy server.
