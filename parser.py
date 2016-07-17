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
            return True
        elif source == 'file' and self.file_regex.match(filename):
            return True
        else:
            return False

    def get_artist_from_file(self, path):
        filename = path.split(os.path.sep)[-1]
        return self.file_regex.match(filename).group('artist')

    def get_title_from_file(self, path):
        filename = path.split(os.path.sep)[-1]
        return self.file_regex.match(filename).group('title')

    def get_label_from_file(self, path):
        filename = path.split(os.path.sep)[-1]
        return self.file_regex.match(filename).group('title')

def build_parsers():
    parsers = []
    # name, album_regex, file_regex
    data = [
            ('thor-test', r'(?P<artist>.+?)_-_(?P<title>.+)', r'(?P<artist>.+?)_-_(?P<title>.+)')
        ]
    for name, album_regex_string, file_regex_string in data:
        p = Parser(name, album_regex_string, file_regex_string)
        parsers.append(p)

    return parsers

