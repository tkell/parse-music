#!/usr/bin/env python
# encoding: utf-8

import os
import re

class Parser():
    def __init__(self, store, album_regex, album_file_regex, single_regex):
        self.store = store
        self.album_regex = re.compile(album_regex)
        self.album_file_regex = re.compile(album_file_regex)
        self.single_regex = re.compile(single_regex)

    def match_store(self, path, source):
        filename = path.split(os.path.sep)[-1]
        if source == 'album' and self.album_regex.search(filename):
            print("Match on album for %s" % self.store)
            return True
        elif source == 'single' and self.single_regex.match(filename):
            print("Match on single for %s" % self.store)
            return True
        else:
            return False

    def get_field(self, path, field, regex_type):
        # Give this the file path
        if regex_type == 'album':
            regex = self.album_regex
        elif regex_type == 'album_file':
            regex = self.album_file_regex
        elif regex_type == 'single':
            regex = self.single_regex
        else:
            raise TypeError("regex_type must be one of album, album_file, or single!")

        filename = path.split(os.path.sep)[-1]
        try:
            return regex.match(filename).group(field)
        except (AttributeError, IndexError):
            print("---- No data in %s for %s.  Please enter the correct string ----" % (path, field))
            r = input()
            return r.strip()

def build_parsers():
    parsers = []

    # name, album_regex, album_file_regex, single_regex
    data = [
            # www.bleep.com
            (
             'bleep', 
             r'(?P<artist>.+?) - (?P<album_title>.+?) - (?P<extension>.+)',
             r'(?P<album_title>.+?)-\d\d\d-(?P<artist>.+?)-(?P<title>.+?)\.(?P<extension>.+)',
             r'(?P<album_title>.+?)-\d\d\d-(?P<artist>.+?)-(?P<title>.+?)\.(?P<extension>.+)'
            ),
            # www.bandcamp.com
            (
              'bandcamp',
              r'(?P<artist>.+?) - (?P<album_title>.+)',
              r'(?P<artist>.+?) - (?P<album_title>.+?) - \d\d (?P<title>.+?)\.(?P<extension>.+)',
              r'(?P<artist>.+?) - (?P<title>.+?)\.(?P<extension>.+)'
            ),
            # www.junodownload.com
            (
              'juno download',
              r'NO EXAMPLES YET',
              r'NO EXAMPLES YET',
              r'(?P<artist>.+?)_-_(?P<title>.+?)\.(?P<extension>.+?)'
            ),
        ]
    for name, album_regex_string, file_regex_string, single_regex_string in data:
        p = Parser(name, album_regex_string, file_regex_string, single_regex_string)
        parsers.append(p)

    return parsers

