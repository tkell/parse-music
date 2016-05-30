#!/usr/bin/env python
# encoding: utf=8

import os
import re

class parser():
    def __init__(self, store):
        self.store = store
        self.regexes = {}

    def match_store(self, path):
        if self.regexes['store'].match(path):
            return True
        else:
            return False

    def add_regex(self, regex, name):
        self.regexes[name] = regex
        


def check_store(path):
    result = []
    for parser in all_parsers:
        if parser.match_store(path):
            result.append(parser.store)
    if len(result) == 1:
        return result[0]
    else:
        pass #panic / disambiguate


def parse_folders(path):
    files = os.listdir(path)
    for filename in files:
        if os.path.isdir(filename):
            parse_folder(filename)

def parse_folder(path):
    store = check_store(path)
    various_artists = check_various_artists(path)
    singles = check_singles(path)
    
    # what regex matches / what store are we from?
    # is this Various Artists or not?
    # is this a singles folder
    for filename in os.listdir(path):
        parse_file(path, filename, store, various_artists, singles)


def parse_file(path, filename, store, various_artists=False, single=False):
    
    pass

def match_tags_to_file(path):
    pass



if __name__ == '__main__':
    parse_folders('.')
