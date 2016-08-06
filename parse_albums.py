#!/usr/bin/env python
# encoding: utf=8

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

from utils import get_context
from utils import check_filetype

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
    context = get_context(path)
    store_parser = check_store(path, parsers)
    if store_parser == None:
        # Eventually we'll deal with errors here,
        # allow the user to enter a store manually, etc
        print "Panic!  No parser found"
        return None

    return path, store_parser, context

def parse_files(folder_path, parser, various_artists=False):
    results = []
    for filename in os.listdir(folder_path):
        filepath = folder_path + os.path.sep + filename
        r = parse_file(filepath, parser, 'regular_album')
        results.extend(r)

    return results 

def parse_albums():
    parsers = build_parsers() # make the objects that pick the store, do lots of other things
    folders = parse_folders('.') # find all the folders we need 
    for folder in folders:
        if folder in ['singles', 'tests']:
            continue
        folder_path, parser, context = parse_folder(folder, parsers) # find all the files, and the flags to parse them
        tasks = parse_files(folder_path, parser, context) # return a list of tuples of files we need to do things to 
        success = do_work(tasks) # rename or re-tag the files, as needed.
        # rename_folder(folder)
