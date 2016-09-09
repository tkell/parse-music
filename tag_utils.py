#!/usr/bin/env python
# encoding: utf=8

## Utils for reading and setting tags
import mutagen

def get_tags(filepath):
    f = mutagen.File(filepath)

    try:
        artist = f.tags['artist'][0]
    except KeyError:
        artist = None

    try:
        title = f.tags['title'][0]
    except KeyError:
        title = None

    return artist, title

def set_tag(filepath, tag_name, tag_content):
    f = mutagen.File(filepath)
    tag_name = tag_name.lower()
    f[tag_name] = tag_content
    f.save()

