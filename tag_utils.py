#!/usr/bin/env python
# encoding: utf=8

## Utils for reading and setting tags
import mutagen

def get_tags(filepath):
    f = mutagen.File(filepath)

    artist = None
    try:
        artist = f.tags['artist'][0]
    except KeyError:
        # stupid amazon
        try: artist = f['TPE2'].text[0]
        except KeyError:
            pass

    title = None
    try:
        title = f.tags['title'][0]
    except KeyError:
        try:
            # stupid amazon
            title = f['TIT2'].text[0]
        except KeyError:
            pass

    return artist, title

def set_tag(filepath, tag_name, tag_content):
    f = mutagen.File(filepath)
    tag_name = tag_name.lower()
    f[tag_name] = tag_content
    f.save()

