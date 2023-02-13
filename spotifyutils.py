import win32gui
from win32gui import GetWindowText, EnumWindows
from win32process import GetWindowThreadProcessId
import psutil
from win11toast import toast
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import tkinter as tk
import wx


class SpotifyUtils:
    def __init__(self):
        self.app = None
        self.spotify_handle = None
        self.last_song = None
        self.current_song = None

        self.ADVERTISEMENT = 'Advertisement'
        self.SPOTIFY_TITLE = 'Spotify Free'

        self.cid = "96a129f9c1274be882af6e1e7efb858a"
        self.secret = "aa7b85ad09bd4551a9dad27db8ae0ced"
        client_credentials_manager = SpotifyClientCredentials(client_id=self.cid, client_secret=self.secret)
        self.sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

        self.get_spotify_handle()

    def get_spotify_handle(self):
        EnumWindows(self.win_enum_handler, None)
        if self.spotify_handle is None:
            return
        title = GetWindowText(self.spotify_handle)
        self.current_song = title.split('-')

    def send_toast(self):
        if self.spotify_handle is None:
            return
        src = self.get_song_image()
        icon = {
            'src': src,
            'placement': 'appLogoOverride'
        }
        print(self.current_song)
        toast(self.current_song[1], self.current_song[0], icon=icon,
              audio={'silent': True})

    def update_song(self):
        if self.spotify_handle is None:
            return
        title = GetWindowText(self.spotify_handle)
        self.current_song = title.split('-')

        if self.current_song == [''] or self.spotify_handle is None:
            self.get_spotify_handle()
            return
        if self.current_song != self.last_song:
            self.last_song = self.current_song
            if self.current_song[0] == self.ADVERTISEMENT or self.current_song[0] == self.SPOTIFY_TITLE:
                print("Advertisement or Paused")
                return
            else:
                self.send_toast()

    def get_song_image(self):
        if self.current_song == [''] or self.spotify_handle is None:
            return
        artist = self.current_song[0].lower()[:-1]
        track = self.current_song[1].lower()[1:]
        image_url = \
            self.sp.search(q='artist:' + artist + ' track:' + track, type='track')['tracks']['items'][0]['album'][
                'images'][
                0]['url']
        return image_url

    def win_enum_handler(self, handle, ctx):
        pid = GetWindowThreadProcessId(handle)[1]
        process_name = psutil.Process(pid).name().lower()
        title = GetWindowText(handle)
        if process_name == "spotify.exe" and (
                len(title.split('-')) > 1 or title == self.ADVERTISEMENT or title == self.SPOTIFY_TITLE):
            spotify_handle = handle
            self.spotify_handle = spotify_handle
