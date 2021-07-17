#!/usr/bin/env python
# encoding: utf=8
import os
import shutil
import re

from parser import build_parsers
from utils import get_context
from utils import move_items
from utils import sort_by_track_number
from work_utils import parse_file
from work_utils import do_work


def parse_folders(path):
    files = os.listdir(path)

    results = []
    for filename in files:
        filepath = path + os.path.sep + filename
        if os.path.isdir(filepath) and filename != 'singles' and filename[0] != '.':
            results.append(filepath)
    return results


def parse_folder(path, parsers):
    context = get_context(path)

    parser = None
    for p in parsers:
        album_string = path.split(os.path.sep)[-1]
        if p.match_store(album_string, source='album'):
            parser = p
            break
    if parser == None:
        # Eventually we'll deal with errors here,
        # allow the user to enter a store manually, etc
        print("Panic!  No parser found")
    else:
        album_info = {}
        album_info['artist'] = parser.get_field(path, 'artist', 'album')
        album_info['album_title'] = parser.get_field(path, 'album_title', 'album')
        album_info['label'] = parser.get_field(path, 'label', 'album')

    return path, parser, context, album_info


def parse_files(folder_path, parser, context, album_info):
    results = []

    filenames = os.listdir(folder_path)
    sorted_filenames = sort_by_track_number(filenames, folder_path, parser)
    for index, filename in enumerate(sorted_filenames):
        if 'mp3' not in filename.lower() and 'flac' not in filename.lower():
            continue

        filepath = os.path.join(folder_path, filename)
        r = parse_file(filepath, parser, context, album_info)
        results.extend(r)
    return results


def rename_folder(folder_path, context, album_info):
    if context == "regular_album":
        artist = album_info['artist']
        title = album_info['album_title']
        label = album_info['label']
        new_folder_name = "%s - %s [%s]" % (artist, title, label)
        path = os.path.dirname(folder_path)
        new_path = os.path.join(path, new_folder_name)
        shutil.move(folder_path, new_path)


def parse_albums(starting_folder, ending_folder, dry_run):
    parsers = (
        build_parsers()
    )  # make the objects that pick the store, do lots of other things
    folders = parse_folders(starting_folder)  # find all the folders we need
    for folder in folders:
        folder_path, parser, context, album_info = parse_folder(
            folder, parsers
        )  # find all the files, and the flags to parse them
        tasks = parse_files(
            folder_path, parser, context, album_info
        )  # return a list of tuples of files we need to do things to
        success = do_work(tasks, dry_run)  # rename or re-tag the files, as needed.
        if not dry_run:
            rename_folder(folder_path, context, album_info)  # very last!

    if not dry_run:
        move_items(starting_folder, ending_folder)
