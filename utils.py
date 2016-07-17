#!/usr/bin/env python
# encoding: utf-8

import os

from tag_utils import get_tags
from tag_utils import set_tag

## Utilities, big and small

def check_various_artists(path):
    folder_name = path.split(os.path.sep)[-1].lower().replace(' ', '')
    if 'variousartists' in folder_name:
        return True
    else:
        return False

def check_filetype(path):
    filename = path.split(os.path.sep)[-1].lower()
    filtype = filename.split('.')[-1]
    if filetype in ['mp3', 'flac']:
        return filetype
    else:
        return None

def do_work(tasks):
    for task in tasks:
        if task[0] == 'rename':
            task_name, filepath, new_filepath  = task
            print new_filepath
            # os.rename(filepath, new_filepath)
        if task[0] == 'retag':
            task_name, filepath, file_artist, file_title = task 
            set_tag(filepath, 'artist', file_artist)
            set_tag(filepath, 'title', file_title)

def make_new_filename(context, data):
    if context == 'single':
        new_filename = "%s - %s [%s].%s" % (data['artist'], data['title'], data['label'], data['extension'])
    ## and many more options to come...

    return new_filename

## might split this out, as it and do_work are not really "utils"
def parse_file(filepath, parser, various_artists=False):
    tag_artist, tag_title = get_tags(filepath) 
    file_artist = parser.get_artist_from_file(filepath)
    file_title = parser.get_title_from_file(filepath)
    file_label = parser.get_label_from_file(filepath)

    work = []

    # if they are the same, we just need to rename the file (unless the parser is 'thor')
    if tag_artist == file_artist and tag_title == file_title:
        new_file_name = make_new_filename('single', {'artist': file_artist, 'title': file_title})
        task = ('rename', new_file_name)
        work.append(task)
    else:
        # If there are tags, we rename
        if tag_artist and tag_title:
            ## dodging label issues now, because they are complicated
            extension = filepath.split('.')[-1]
            new_file_name = make_new_filename('single', {'artist': tag_artist,
                                                        'title': tag_title,
                                                        'label': '',
                                                        'extension': extension
                                                        })
            print new_file_name
            folder_path = os.path.join(os.path.split(filepath)[0:-1])[0]
            new_filepath = os.path.join(folder_path, new_file_name)
            task = ('rename', filepath, new_filepath)
            work.append(task)
        # if there are no tags, we set the tags, then rename the file.
        else:
            task = ('retag', filepath, file_artist, file_title)
            work.append(task)
            new_file_name = make_new_filename('single', {'artist': tag_artist, 'title': tag_title, 'label': ''})
            task = ('rename', filepath, new_file_name)
            work.append(task)

    return work
