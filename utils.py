#!/usr/bin/env python
# encoding: utf-8

## Utilities, big and small
from tag_utils impot get_tags

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

def make_new_filename(context, data):
    if context == 'single':
        new_filename = "%s - %s [%s]" % (data['artist'], data['title'], data['label'])
    ## and many more options to come...

    return new_filename

## might split this out, as it and do_work are not really "utils"
def parse_file(filepath, parser, various_artists=False):
    tag_artist, tag_title = get_tags(filepath) 
    file_artist = parser.get_artist_from_file(filepath)
    file_title = parser.get_title_from_file(filepath))
    file_label = parser.get_label_from_file(filepath))

    work = []

    # if they are the same, we just need to rename the file (unless the parser is 'thor')
    if tag_artist == file_artist and tag_title == file_title:
        new_file_name = make_new_filename('single', {'artist': file_artist, 'title': file_title})
        task = ('rename', new_file_name)
        work.append(task)
    else:
        # If there are no tags, we retag and then rename
        if tag_artist and tag_title:
            new_file_name = make_new_filename('single', {'artist': tag_artist, 'title': tag_title})
            task = ('rename', filepath, new_file_name)
            work.append(task)
            task = ('retag', filepath, filetype, file_artist, file_title)
            work.append(task)
        # if there are tags, we rename the file
        elif f == 't':
            new_file_name = make_new_filename('single', {'artist': tag_artist, 'title': tag_title})
            task = ('rename', filepath, new_file_name)
            work.append(task)

    return work
