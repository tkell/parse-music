#!/usr/bin/env python
# encoding: utf=8

## Utils for reading and setting tags
import taglib

def get_tags(filepath):
    f = taglib.File(filepath)

    try:
        artist = f.tags['ARTIST'][0]
    except KeyError:
        artist = None

    try:
        title = f.tags['TITLE'][0]
    except KeyError:
        title = None

    return artist, title

def set_tag(filepath, tag_name, tag_content):
    f = taglib.File(filepath)
    tag_name = tag_name.upper()
    f.tags[tag_name] = tag_content
    f.save()

