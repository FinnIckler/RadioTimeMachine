from glob import iglob
import random

import mutagen
import mutagen.mp3
import os
import re
import calendar


class UnsupportedFormatError(Exception):
    def __init__(self, message, errors):
        super(UnsupportedFormatError, self).__init__(message)
        self.errors = errors


class LibraryHandler:
    base_path = ""
    FIRSTYEAR = 1920 # Should indicate the first year of your music library.
    LASTYEAR = 2017  # Should indicate the current year
    _years = [i for i in range(FIRSTYEAR, LASTYEAR, 1)]
    # The Library consists of an array of dictionaries for each month of the year
    _library = [[{} for j in range(0, 12, 1)] for i in range(FIRSTYEAR, LASTYEAR, 1)]

    def __init__(self, base_path):
        self.base_path = base_path
        self._build_library()

    def get_music_from_year_month(self, year, month):
        """Look up the songs in the library and chose a random one
        @:returns the song or None if the library doesn't have a song from that month/year"""
        month_library = self._library[year - self.FIRSTYEAR - 1][month - 1]
        if month_library:
            track_no = random.choice(list(month_library.keys()))
            return month_library[track_no]
        else:
            return None

    def _build_library(self):
        """Goes through every file in the given folder and adds them to the library if they are correctly tagged"""
        for f in iglob(self.base_path + "/**/*", recursive=True):
            try:
                result = self._parse_tag(f)
            except UnsupportedFormatError:
                print("Mistagged file", f)
            if not result:
                continue
            else:
                year_index = result['year'] - self.FIRSTYEAR - 1
                month_index = result['month'] - 1
                try:
                    self._library[year_index][month_index][result['file']] = result
                except:
                    raise RuntimeError("Failed for:"+ result['file'])
                print("added", result['file'])

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
        if {"TIT3", "TPE1", "TDRC", "TALB"}.issubset(set(tags.keys())):
            year = tags['TDRC'].text[0]
            if type(year) != str:
                year = year.text
                try:
                    int(year)
                except:
                    return False
            return {
                "file": filename,
                'date': tags['TIT3'].text[0],
                'artist': tags['TPE1'].text[0],
                'album': tags['TALB'].text[0],
                'year': int(year),
                'month': self._get_month(tags['TIT3'].text[0])
            }
        else:
            return False

    def _get_month(self, date):
        """Extracts the Month from the tag. To different Formats are accepted dd-Mon-yyyy and yyyy-mm-dd.
        If the song had an unreadable description tag, a UnsupportedFormatError is raised"""
        try:
            if len(date.split(" ")) == 3:
                year, month, day = date.split(" ")
                month_reg = re.compile("Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec")
                if re.match(month_reg, month):
                    return list(calendar.month_abbr).index(month)
                else:
                    int(month)
                    return int(month)
            else:
                year, month = date.split(" ")
                if re.match(re.compile("Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec"), month):
                    return list(calendar.month_abbr).index(month)
                else:
                    return int(month)
        except Exception:
            raise UnsupportedFormatError("The Description Tag is not correctly formatted, the supported formats are "
                                         "dd-Mon-yyyy and yyyy-mm-dd. The date was: "+date,Exception)

    def _parse_tag(self, f):
        """Parses the Tags from a given .mp3 file
        @:returns a Dictionary of Tags or False if the file is not a music file"""
        if not os.path.isdir(f):
            try:
                tags = mutagen.File(f)
            except mutagen.mp3.HeaderNotFoundError:
                print("Failed for: ", f)
                return False
            if tags is not None:
                return self._data_entry(tags, f)
            else:
                return False
        else:
            return False
