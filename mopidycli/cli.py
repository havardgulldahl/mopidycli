from __future__ import unicode_literals

import jsonrpclib



#             'mopidy-state = mopidycli.cli:state',
#             'mopidy-play = mopidycli.cli:play',
#             'mopidy-pause = mopidycli.cli:pause',
#             'mopidy-resume = mopidycli.cli:resume',
#             'mopidy-next = mopidycli.cli:next',
#             'mopidy-previous = mopidycli.cli:previous',
#             'mopidy-tracklist = mopidycli.cli:tracklist',
#             'mopidy-shuffle = mopidycli.cli:shuffle',
#         ],


def getServer():
    return jsonrpclib.Server('http://192.168.0.182:6680/mopidy/rpc')

def formatTimeposition(milliseconds):
    seconds = milliseconds//1000.0
    min_part = seconds // 60.0
    sec_part = seconds % 60.0
    return '{}:{}'.format(min_part, sec_part)

def state():
    '''Get The playback state: PLAYING, PAUSED, or STOPPED.

    If PLAYING or PAUSED, show information on current track.

    Calls PlaybackController.get_state(), and if state is PLAYING or PAUSED, get
      PlaybackController.get_current_track() and
      PlaybackController.get_time_position()'''

    server = getServer()
    state = server.core.playback.get_state()
    logger.debug('Got playback state: %r', state)
    if state == 'STOPPED':
        print('Playback is currently stopped')
    else:
        track = server.core.playback.get_current_track()
        pos = server.core.playback.get_time_position()
        print('{} track: "{}", by {} (at {})'.format(state.title(),
                                                     track.title,
                                                     track.artists,
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
    for tlid, t in getServer().core.tracklist.get_tl_tracks():
        print('{}: {}'.format(tlid, t.title))


  def shuffle():
    '''Shuffles the entire tracklist.

    Calls TracklistController.shuffle(start=None, end=None)'''

    return getServer().core.tracklist.shuffle()
