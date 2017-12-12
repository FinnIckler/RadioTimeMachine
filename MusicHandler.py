import vlc
import LibraryHandler


class MusicHandler:
    _player = None
    _path = None
    _lib_handler = None
    BASE_PATH = ""

    def _play_music(self, path):
        """Internal method for playing music, either creates a new VLC Player instance and plays the music
        or changes the music in the already existing instance"""
        if self._player is None:
            self._player = vlc.MediaPlayer(path)
            self._path = path
        else:
            self._player.stop()
            self._player.set_mrl(path)
            self._path = path
        self._player.play()

    def __init__(self,path):
        self.BASE_PATH = path
        self._lib_handler = LibraryHandler.LibraryHandler(self.BASE_PATH)

    def play_music(self, year, month):
        """Plays music from a specific month and year
        @:returns the name of the played file or None if no new track is played,
        this return value can be used for displaying the current track"""
        track = self._lib_handler.get_music_from_year_month(year, month)
        if track is not None:
            self._play_music(track['file'])
            return track['file']
        else:
            return None
