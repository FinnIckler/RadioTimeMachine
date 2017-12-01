import vlc
import LibraryHandler


class MusicHandler:
    _player = None
    _path = None
    _lib_handler = None
    BASE_PATH = ""

    def _play_music(self, path):
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
        self._lib_handler.get_music_from_year_month(year, month)
