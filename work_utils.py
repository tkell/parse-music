#!/usr/bin/env python
# encoding: utf-8


import os
import tag_utils


def parse_file(filepath, parser, context, album_info=None):
    ## This is where I was going to deal with the shit, basically - using context as a switch
    # The context defines where we get the data we need, and what we might rename the file
    # It is the parser's job to get the data - if we have to ask the user for it, the parser can do that
    # should I have one parser per store per context?  Or just two per store albums / singles?
    if context == "single":
        tag_artist, tag_title = tag_utils.get_tags(filepath)

        # Juno is stupid and has all-caps artist names.
        # We correct that and re-write the tag here, ugh.
        if parser.store == "juno download":
            artist_words = tag_artist.split(" ")
            artist_words = [word.lower() for word in artist_words]
            artist_words = [word[0].upper() + word[1:] for word in artist_words]
            tag_artist = " ".join(artist_words)
            tag_utils.set_tag(filepath, "artist", tag_artist)

        file_artist = parser.get_field(filepath, "artist", "single")
        file_title = parser.get_field(filepath, "title", "single")
        file_label = parser.get_field(filepath, "label", "single")
        extension = filepath.split(os.path.sep)[-1].split(".")[-1].lower()
        new_name_from_file = "%s - %s [%s].%s" % (
            file_artist,
            file_title,
            file_label,
            extension,
        )
        new_name_from_tag = "%s - %s [%s].%s" % (
            tag_artist,
            tag_title,
            file_label,
            extension,
        )
    elif context == "regular_album":
        tag_artist, tag_title = tag_utils.get_tags(filepath)
        file_artist = album_info["artist"]
        file_title = parser.get_field(filepath, "title", "album_file")
        file_track_number = int(
            parser.get_field(filepath, "track_number", "album_file")
        )
        file_label = album_info["label"]
        extension = filepath.split(os.path.sep)[-1].split(".")[-1].lower()
        new_name_from_file = "%02d - %s.%s" % (file_track_number, file_title, extension)
        new_name_from_tag = "%02d - %s.%s" % (file_track_number, tag_title, extension)
    elif context == "various_artists_album":
        tag_artist, tag_title = tag_utils.get_tags(filepath)
        file_artist = parser.get_field(filepath, "artist", "various_artists_file")
        file_title = parser.get_field(filepath, "title", "various_artists_file")
        file_track_number = int(
            parser.get_field(filepath, "track_number", "various_artists_file")
        )
        file_label = album_info["label"]
        extension = filepath.split(os.path.sep)[-1].split(".")[-1].lower()
        # We only use the name from the file,
        # as there are lots of strange metadata things in Various Artists albums
        new_name_from_file = "%02d - %s - %s.%s" % (
            file_track_number,
            file_artist,
            file_title,
            extension,
        )
        new_name_from_tag = new_name_from_file
    else:
        pass

    work = select_work(
        filepath,
        tag_artist,
        tag_title,
        file_artist,
        file_title,
        new_name_from_file,
        new_name_from_tag,
    )
    return work


def select_work(
    filepath,
    tag_artist,
    tag_title,
    file_artist,
    file_title,
    new_name_from_file,
    new_name_from_tag,
):
    work = []

    # if they are the same, we just need to rename the file
    if tag_artist == file_artist and tag_title == file_title:
        new_file_name = new_name_from_file
        folder_path = os.path.split(filepath)[0:-1][0]
        new_filepath = os.path.join(folder_path, new_file_name)
        task = ("rename", filepath, new_filepath)
        work.append(task)
    else:
        # If there are tags, we rename based on the tag
        if tag_artist and tag_title:
            filepath.split(".")[-1]
            new_file_name = new_name_from_tag
            folder_path = os.path.split(filepath)[0:-1][0]
            new_filepath = os.path.join(folder_path, new_file_name)
            task = ("rename", filepath, new_filepath)
            work.append(task)
        # if there are no tags, we set the tags, then rename the file
        else:
            task = ("retag", filepath, file_artist, file_title)
            work.append(task)
            new_file_name = new_name_from_file

            folder_path = os.path.split(filepath)[0]
            new_file_path = os.path.join(folder_path, new_file_name)
            task = ("rename", filepath, new_file_path)
            work.append(task)

    return work


def do_work(tasks, dry_run):
    for task in tasks:
        if task[0] == "rename":
            task_name, filepath, new_filepath = task
            if not dry_run:
                os.rename(filepath, new_filepath)
            else:
                print("Would do ", task)
        if task[0] == "retag":
            task_name, filepath, artist, title = task
            if not dry_run:
                tag_utils.set_tag(filepath, "artist", artist)
                tag_utils.set_tag(filepath, "title", title)
            else:
                print("Would do ", task)

    return True  ## Catch exceptions here, as they show up.
