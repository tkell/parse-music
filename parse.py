#!/usr/bin/env python
# encoding: utf=8

## singles are Artist - Title (Remix) [Label]
## albums are Artist - Title [Label]
## album tracks are Track Number - Title
## VA albums are Various Artists - Title [Label]
## VA album tracks are Track Number - Artist - Title
## Composer albums are Composer - Title (Performer) [Label]
## composer album tracks are Track Number - Title
## VA albums with composer tracks are Track Number - Composer - Title (Performer)
## Performer albums are Performer - Title [Label] 
## Performer album tracks are Track Number - Title (Composer)


import os
import re

import eyed3

from utils import check_singles
from utils import check_various_artists
from utils import check_filetype

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

    return path, store_parser, singles, various_artists

def parse_files(folder_path, parser, various_artists=False):
    results = []
    for filename in os.listdir(folder_path):
        filepath = folder_path + os.path.sep + filename
        r = parse_file(filepath, parser, various_artists)
        results.extend(r)

    return results 


def get_tags(filetype, filepath):
    if filetype == 'mp3':
        audiofile = eyed3.load(filepath) ### use taglib!
        artist = audiofile.tag.artist
        title = audiofile.tag.title
    elif filetype == 'flac':
        pass

    return artist, title


def parse_file(filepath, parser, various_arists):

    filetype = check_filetype(filepath) 
    tag_artist, tag_title = get_tags(filetype, filepath) 
    file_artist = parser.get_artist(filepath, various_artists)
    file_title = parser.get_title(filepath, various_artists)

    work = []

    # if they are the same, we just need to rename the file (unless the parser is 'thor')
    if tag_artist == file_artist and tag_title == file_title:
        new_file_name = make_new_filename(file_artist, file_title, various_artists)
        task = ('rename', new_file_name)
        work.append(task)
    else:
        # if they are not the same, we need to pick who wins.  Ask the user?
        # match file to tags
        # match tags to file
        t = get_user_input(filepath, tag_artist, tag_title, file_artist, file_title)
        if t == 'match_file_to_tags':
            new_file_name = make_new_filename(file_artist, file_title, various_artists)
            task = ('rename', filepath, new_file_name)
            work.append(task)
        elif t == 'match_tags_to_file':
            task = ('retag', filepath, filetype, file_artist, file_title)
            work.append(task)

    return work

def parse_singles(folder_path, parsers):
    # need to check each damn file to find the right parser, alas
    pass


def do_work(tasks):
    ## returns array of success / fail for each task
    results = []
    for task in tasks:
        if task[0] == 'rename':
            task_name, filepath, new_file_name = task
            r = rename_file(filepath, new_file_name)
        if task[0] == 'retag':
            task_name, filetype, file_artist, file_title = task 
            r = retag_file(filepath, filetype, file_artist, file_title) 
    return results


if __name__ == '__main__':
    parsers = build_parsers() # make the objects that pick the store, do lots of other things
    folders = parse_folders('.') # find all the folders we need 
    for folder in folders:
        path, parser, singles, various_artists = parse_folder(folder, parsers) # find all the files, and the flags to parse them
        if singles:
            tasks = parse_singles(path, parser)
        else:
            tasks = parse_files(path, parser, various_artists) # return a list of tuples of files we need to do things to 
        success = do_work(tasks) # rename or re-tag the files, as needed.
        `
