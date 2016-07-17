#!/usr/bin/env python
# encoding: utf=8

## Utils for reading and setting tags
import taglib

def get_tags(filepath):
    f = taglib.File(filepath)
    return f.tags['ARTIST'], f.tags['TITLE']
    
def set_tag(filepath, tag_name, tag_content):
    f = taglib.File(filepath)
    tag_name = tag_name.upper()
    f.tags[tag_name] = tag_content
    f.save()

