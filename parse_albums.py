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

from parser import build_parsers
from utils import get_context
from work_utils import parse_file
from work_utils import do_work

def parse_folders(path):
    files = os.listdir(path)

    results = []
    for filename in files:
        filepath = path + os.path.sep + filename
        if os.path.isdir(filepath) and filename != 'singles' and filename[0] != '.':
            results.append(filepath)
    return results 

def parse_folder(path, parsers):
    context = get_context(path)

    parser = None
    for p in parsers:
        album_string = path.split(os.path.sep)[-1]
        print album_string
        if p.match_store(album_string, source='album'):
            parser = p
            break
    if parser == None:
        # Eventually we'll deal with errors here,
        # allow the user to enter a store manually, etc
        print "Panic!  No parser found"
    else:
        album_info = {}
        album_info['artist'] = parser.get_field_from_album(path, 'artist')
        album_info['title'] = parser.get_field_from_album(path, 'album_title')
        album_info['label'] = parser.get_field_from_album(path, 'label')

    return path, parser, context, album_info

def parse_files(folder_path, parser, context, album_info):
    results = []
    # We assume that the files are in the correct order
    for index, filename in enumerate(os.listdir(folder_path)):
        if 'mp3' not in filename.lower() and 'flac' not in filename.lower():
            continue

        filepath = folder_path + os.path.sep + filename
        track_number = index + 1
        r = parse_file(filepath, parser, 'regular_album', track_number, album_info)
        results.extend(r)
    return results 

def parse_albums(starting_folder):
    parsers = build_parsers() # make the objects that pick the store, do lots of other things
    folders = parse_folders(starting_folder) # find all the folders we need 
    for folder in folders:
        folder_path, parser, context, album_info = parse_folder(folder, parsers) # find all the files, and the flags to parse them
        tasks = parse_files(folder_path, parser, context, album_info) # return a list of tuples of files we need to do things to 
        success = do_work(tasks) # rename or re-tag the files, as needed.
        # rename_folder(folder_path, album_info) # very last!
