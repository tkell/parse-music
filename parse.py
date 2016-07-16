#!/usr/bin/env python
# encoding: utf=8

import os
import re



class Parser():
    def __init__(self, store, regex):
        self.store = store
        self.regex = re.compile(regex)

    def match_store(self, path):
        filename = path.split(os.path.sep)[-1]
        if self.regex.match(filename):
            return True
        else:
            return False

def build_parsers():
    parsers = []
    data = {'thor': r'(.+) - (.+)'} # Artist - Title, just a tester
    for name, regex_string in data.items():
        p = Parser(name, regex_string)
        parsers.append(p)

    return parsers

def check_store(path, parsers):
    result = []
    for parser in parsers:
        if parser.match_store(path):
            result.append(parser)
    if len(result) == 1:
        return result[0]
    else:
        return None # panic / disambiguate!

def check_singles(path):
    if path.split(os.path.sep)[-1] == 'Singles':
        return True
    else:
        return False

def check_various_artists(path):
    folder_name = path.split(os.path.sep)[-1].lower().replace(' ', '')
    if 'variousartists' in folder_name:
        return True
    else:
        return False


def parse_folders(path):
    current_dir = os.getcwd()
    files = os.listdir(path)

    results = []
    for filename in files:
        filepath = current_dir + os.path.sep + filename
        if os.path.isdir(filepath) and filename[0] != '.':
            results.append(filepath)

    return results 

def parse_folder(path, parsers):
    singles = check_singles(path)
    various_artists = check_various_artists(path)
    store_parser = check_store(path, parsers)
    if store_parser == None:
        # Eventually we'll deal with errors here,
        # allow the user to enter a store manually, etc
        return None

    print singles, various_artists, store_parser.store
    return path, store_parser, singles, various_artists
    
    # what regex matches / what store are we from?
    # is this Various Artists or not?
    # is this a singles folder
    for filename in os.listdir(path):
        parse_file(path, filename, store, various_artists, singles)


def parse_files(folder_path, parser, various_artists=False, single=False):
    pass

def match_tags_to_file(path):
    pass



if __name__ == '__main__':
    parsers = build_parsers() # make the objects that pick the store, do lots of other things
    folders = parse_folders('.') # find all the folders we need 
    for folder in folders:
        path, parser, singles, various_artists = parse_folder(folder, parsers) # find all the files, and the flags to parse them
        work_to_do = parse_files(path, parser, singles, various_artists) # return a list of tuples of files we need to do things to -- user input happens here
        success = do_work(work_to_do) # rename or re-tag the files, as needed
