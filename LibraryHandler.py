from glob import iglob
from random import random

import mutagen
import mutagen.mp3
import os


class LibraryHandler:
    base_path = ""
    FIRSTYEAR = 1920
    LASTYEAR = 2017
    _years = [i for i in range(FIRSTYEAR, LASTYEAR, 1)]
    _library = [[{} for j in range(1, 12, 1)] for i in range(FIRSTYEAR, LASTYEAR, 1)]

    def __init__(self, base_path):
        self.base_path = base_path
        self._build_library()

    def get_music_from_year_month(self, year, month):
        month_library = self._library[year - self.FIRSTYEAR][month - 1]
        track_no = random(0, len(month_library))
        return month_library.items()[track_no]

    def _build_library(self):
        for f in iglob(self.base_path + "/**/*", recursive=True):
            result = self._parse_tag(f)
            if not result:
                continue
            else:  # Year scaled down               Month scaled down      Library Entry
                self._library[result['year'] - self.FIRSTYEAR][result['month'] - 1][result['filename']] = result

    def _data_entry(self, tags, filename):
        """
        Gets the Entries out of the Tags:
        @:returns
           The Description ID3 Tag is Saved in the TIT3 Block
           The Artist ID3 Tag is Saved in the TPE1 Block
           The Album ID3 Tag is Saved in the TALB Block
           The Cover image is Saved in the APIC: Block
           The Year is Saved in the TDRC Block
           The Genre ID3 Tag is Saved in the TCON Block
           or False if the file does not include the tags"""
        if set("TIT3,TPE1,TALB,TCON,TDRC").issubset(set(tags.keys())):
            return {
                "file": filename,
                'date': tags['TIT3'].text[0],
                'artist': tags['TPE1'].text[0],
                'album': tags['TALB'].text[0],
                'genre': tags['TCON'].text[0],
                'year': int(tags['TDRC'].text[0]),
                'month': self._get_month(tags['TIT3'].text[0])
            }
        else:
            return False

    def _get_month(self, date):
        if len(date.split(" ")) == 3:
            day, month, year = date.split(" ")
            return int(month)
        else:
            month, year = date.split(" ")
            return int(month)

    def _parse_tag(self, f):
        """Parses the Tags from a given .mp3 file
        @:returns a Dictionary of Tags or False"""
        if not os.path.isdir(f):
            try:
                tags = mutagen.File(f)
            except mutagen.mp3.HeaderNotFoundError:
                print("Failed for: ", f)
                return False
            return self._data_entry(tags, f)
        else:
            return False
