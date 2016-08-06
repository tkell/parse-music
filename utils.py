#!/usr/bin/env python
# encoding: utf-8

import os

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

