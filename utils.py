#!/usr/bin/env python
# encoding: utf=8

## Utils that don't go in the parser itself

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

def check_filetype(path)
    filename = path.split(os.path.sep)[-1].lower()
    filtype = filename.split('.')[-1]
    if filetype in ['mp3', 'flac']:
        return filetype
    else:
        return None
