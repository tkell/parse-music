#!/usr/bin/env python
# encoding: utf-8


import os
import tag_utils

def parse_file(filepath, parser, context, track_number=None, album_info=None):
    ## This is where I was going to deal with the shit, basically - using context as a switch
    # The context defines where we get the data we need, and what we might rename the file
    # It is the parser's job to get the data - if we have to ask the user for it, the parser can do that
    # should I have one parser per store per context?  Or just two per store albums / singles?
    if context == 'single':
        tag_artist, tag_title = tag_utils.get_tags(filepath) 
        file_artist = parser.get_field_from_file(filepath, 'artist')
        file_title = parser.get_field_from_file(filepath, 'title')
        file_label = parser.get_field_from_file(filepath, 'label')
        extension = filepath.split(os.path.sep)[-1].split('.')[-1].lower()
        new_name_from_file = "%s - %s [%s].%s" % (file_artist, file_title, file_label, extension)
        new_name_from_tag = "%s - %s [%s].%s" % (tag_artist, tag_title, file_label, extension)
    elif context == "regular_album":
        tag_artist, tag_title = tag_utils.get_tags(filepath)
        file_artist = album_info['artist']
        file_title = parser.get_field_from_file(filepath, 'title')
        file_label = album_info['label']
        extension = filepath.split(os.path.sep)[-1].split('.')[-1].lower()
        new_name_from_file = "%02d - %s.%s" % (track_number, file_title, extension)
        new_name_from_tag = "%02d - %s.%s" % (track_number, tag_title, extension)
    else:
        pass

    work = select_work(filepath, tag_artist, tag_title, file_artist, file_title, new_name_from_file, new_name_from_tag)

    return work

def select_work(filepath, tag_artist, tag_title, file_artist, file_title, new_name_from_file, new_name_from_tag):
    work = []

    # if they are the same, we just need to rename the file
    if tag_artist == file_artist and tag_title == file_title:
        new_file_name = new_name_from_file
        folder_path = os.path.split(filepath)[0:-1][0]
        new_filepath = os.path.join(folder_path, new_file_name)
        task = ('rename', filepath, new_filepath)
        work.append(task)
    else:
        # If there are tags, we rename based on the tag
        if tag_artist and tag_title:
            extension = filepath.split('.')[-1]
            new_file_name = new_name_from_tag
            folder_path = os.path.split(filepath)[0:-1][0]
            new_filepath = os.path.join(folder_path, new_file_name)
            task = ('rename', filepath, new_filepath)
            work.append(task)
        # if there are no tags, we set the tags, then rename the file
        else:
            task = ('retag', filepath, file_artist, file_title)
            work.append(task)

            new_file_name = new_name_from_file
            folder_path = os.path.join(os.path.split(filepath)[0:-1])[0]
            new_file_path = os.path.join(folder_path, new_file_name)
            task = ('rename', filepath, new_file_path)
            work.append(task)

    return work

def do_work(tasks):
    for task in tasks:
        if task[0] == 'rename':
            task_name, filepath, new_filepath  = task
            os.rename(filepath, new_filepath)
        if task[0] == 'retag':
            task_name, filepath, artist, title = task 
            tag_utils.set_tag(filepath, 'artist', artist)
            tag_utils.set_tag(filepath, 'title', title)

    return True ## Catch exceptions here, as they show up.
