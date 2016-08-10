#!/usr/bin/env python
# encoding: utf-8

import os
import shutil

def check_various_artists(path):
    folder_name = path.split(os.path.sep)[-1].lower().replace(' ', '')
    if 'variousartists' in folder_name:
        return True
    else:
        return False

def check_filetype(path):
    filename = path.split(os.path.sep)[-1].lower()
    filetype = filename.split('.')[-1]
    if filetype in ['mp3', 'flac']:
        return filetype
    else:
        return None

def get_context(path):
    ## This will eventually return one string for each possible album type
    ## but for now:
    return 'regular_album'

def move_items(starting_path, ending_path):
    # Take folders, mp3s, and flacs, and move them.  Ignore folders name 'singles'
    for filename in os.listdir(starting_path):
        filepath = os.path.join(starting_path, filename)
        ending_filepath = os.path.join(ending_path, filename)
        if os.path.isdir(filepath) and filename != 'singles':
            shutil.move(filepath, ending_filepath)
        elif '.mp3' in filename.lower() or '.flac' in filename.lower():
            shutil.move(filepath, ending_filepath)
