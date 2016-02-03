from __future__ import unicode_literals

import sys
import os
import logging
logging.basicConfig(level=logging.INFO)
import argparse
import jsonrpclib

## HELPER FUNCTIONS ##

def getServer():
    ip = os.environ.get('MOPIDYSERVER', '127.0.0.1:6680')
    return jsonrpclib.Server('http://{}/mopidy/rpc'.format(ip))

def formatTimeposition(milliseconds):
    seconds = milliseconds//1000.0
    min_part = seconds // 60.0
    sec_part = seconds % 60.0
    return '{:n}:{:02n}'.format(min_part, sec_part)

def parse_args_and_apply_logging_level(parser, argv):
    args = parser.parse_args(argv)
    logging.basicConfig(level=getattr(logging, args.loglevel.upper()))
    logging.captureWarnings(True)
    #http_client.HTTPConnection.debuglevel = 1 if args.loglevel == 'debug' else 0
    return args

## FUNCTIONS EXPOSED TO CLI ##

def state():
    '''Get The playback state: 'playing', 'paused', or 'stopped'.

    If PLAYING or PAUSED, show information on current track.

    Calls PlaybackController.get_state(), and if state is PLAYING or PAUSED, get
      PlaybackController.get_current_track() and
      PlaybackController.get_time_position()'''

    server = getServer()
    state = server.core.playback.get_state()
    logging.debug('Got playback state: %r', state)
    if state.upper() == 'STOPPED':
        print('Playback is currently stopped')
    else:
        track = server.core.playback.get_current_track()
        logging.debug('Track is %r', track)
        logging.debug('Track loaded is %r', jsonrpclib.jsonclass.load(track))
        pos = server.core.playback.get_time_position()
        logging.debug('Pos is %r', pos)
        print('{} track: "{}", by {} (at {})'.format(state.title(),
                                                     track['name'],
                                                     ','.join([a['name'] for a in track['artists']]),
                                                     formatTimeposition(pos))
              )


def play():
    '''play the currently active track.

    Calls PlaybackController.play(None, None)'''

    return getServer().core.playback.play()

def pause():
    '''Pause playback.

    Calls PlaybackController.pause()'''

    server = getServer()
    server.core.playback.pause()
    pos = server.core.playback.get_time_position()
    print('Paused at {}'.format(formatTimeposition(pos)))

def resume():
    '''If paused, resume playing the current track.

    Calls PlaybackController.resume()'''

    return getServer().core.playback.resume()


def next():
    '''Change to the next track.

    The current playback state will be kept.
    If it was playing, playing will continue. If it was paused, it will still be paused, etc.

    Calls PlaybackController.next()'''

    return getServer().core.playback.next()

def previous():
    '''Change to the previous track.

    The current playback state will be kept.
    If it was playing, playing will continue. If it was paused, it will still be paused, etc.

    Calls PlaybackController.previous()'''

    return getServer().core.playback.previous()

def tracklist():
    '''Get tracklist

    Calls TracklistController.get_tl_tracks()
    '''
    _c = 0
    server = getServer()
    _current = server.core.tracklist.index()
    for t in server.core.tracklist.get_tl_tracks():
        logging.debug('Got tl trak: %r', t)
        currently = ' -- CURRENT' if t['tlid'] == _current else ''
        print('{}: {}{}'.format(t['tlid'], t['track']['name'], currently))
        _c = _c+1
    print('==='*6)
    print('{} tracks in tracklist'.format(_c))


def shuffle():
    '''Shuffles the entire tracklist.

    Calls TracklistController.shuffle(start=None, end=None)'''

    return getServer().core.tracklist.shuffle()


def play_backend_uri(argv=None):
    '''Get album or track from backend uri and play all tracks found.

    uri is a string which represents some directory belonging to a backend.

    Calls LibraryController.browse(uri) to get an album and LibraryController.lookup(uri)
    to get track'''

    if argv is None:
        argv = sys.argv[1:]
    parser = argparse.ArgumentParser(description='Browse directories and tracks at the given uri and play them/it.')
    parser.add_argument('uri',
                        help='The key that represents some directory belonging to a backend. E.g. plex:album:2323 or spotify:album:xxxx')
    parser.add_argument('-l', '--loglevel', help='Logging level. Default: %(default)s.',
        choices=('debug', 'info', 'warning', 'error'), default='warning')
    args = parse_args_and_apply_logging_level(parser, argv)
    server = getServer()
    hits = server.core.library.browse(args.uri)
    # browse(): Returns a list of mopidy.models.Ref objects for the directories and tracks at the given uri.
    logging.info('Got hits from browse(): %r', hits)
    if len(hits) == 0:
        # try track lookup
        hits = server.core.library.lookup(args.uri)
        logging.info('Got hits from lookup() : %r', hits)

    if len(hits) == 0:
        print('No hits for "{}"'.format(args.uri))
    else:
        server.core.tracklist.clear()
        logging.debug('got special uris: %r', [t['uri'] for t in hits])
        server.core.tracklist.add(uris=[t['uri'] for t in hits])
        server.core.playback.play()
