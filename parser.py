#!/usr/bin/env python
# encoding: utf-8

import os
import re

class Parser():
    def __init__(self, store, album_regex, file_regex):
        self.store = store
        self.album_regex = re.compile(album_regex)
        self.file_regex = re.compile(file_regex)

    def match_store(self, path, source):
        filename = path.split(os.path.sep)[-1]
        if source == 'album' and self.album_regex.search(filename):
            print("Match on album for %s" % self.store)
            return True
        elif source == 'file' and self.file_regex.match(filename):
            return True
        else:
            return False

    def get_field_from_file(self, path, field):
        # Give this the file path
        filename = path.split(os.path.sep)[-1]
        try:
            return self.file_regex.match(filename).group(field)
        except (AttributeError, IndexError):
            print("---- No data in %s for %s.  Please enter the correct string ----" % (path, field))
            r = input()
            return r.strip()

    def get_field_from_album(self, path, field):
        # Give this the album path
        folder_name = path.split(os.path.sep)[-1]
        try:
            return self.album_regex.match(folder_name).group(field)
        except (AttributeError, IndexError):
            print("---- No data in %s for %s.  Please enter the correct string ----" % (path, field))
            r = input()
            return r.strip()

def build_parsers():
    parsers = []
    # name, album_regex, file_regex
    ## Will we need a 'single regex'?  Will depend on the store, I betcha =\
    # so I need to replace boomkat with juno download and amazon

    data = [
            # www.bleep.com
            (
             'bleep', 
             r'(?P<artist>.+?) - (?P<album_title>.+?) - (?P<extension>.+?)',
             r'(?P<album_title>.+?)-\d\d\d-(?P<artist>.+?)-(?P<title>.+?)\.(?P<extension>.+?)'
            ),
            # www.bandcamp.com
            (
              'bandcamp',
              r'(?P<artist>.+?) - (?P<album_title>.+?)',
              r'(?P<artist>.+?) - (?P<title>.+?)\.(?P<extension>.+?)'
            ),
            # www.junodownload.com
            (
              'juno download',
              r'NO EXAMPLES YET', 
              r'(?P<artist>.+?)_-_(?P<title>.+?)\.(?P<extension>.+?)'
            ),
            # www.amazon.com
            (
              'amazon ',
              r'NO EXAMPLES / SUPER GENERIC',
              r'\d\d - (?P<title>.+?)\.(?P<extension>.+)'
            ),
        ]
    for name, album_regex_string, file_regex_string in data:
        p = Parser(name, album_regex_string, file_regex_string)
        parsers.append(p)

    return parsers

