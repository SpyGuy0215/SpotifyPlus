from win32gui import GetWindowText, EnumWindows
from win32process import GetWindowThreadProcessId
import psutil
import re
from win11toast import toast
import spotipy
import time

from spotifyutils import SpotifyUtils

su = SpotifyUtils()

VERSION = '1.0.0'
AUTHOR = 'SpyGuy0215'

if __name__ == '__main__':
    while True:
        if su.spotify_handle is None:
            su.get_spotify_handle()
        else:
            su.update_song()
            time.sleep(0.2)



