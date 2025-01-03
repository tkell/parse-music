#!/usr/bin/env python
# encoding: utf-8

import os
import re


class Parser:
    def __init__(
        self,
        store,
        album_regex,
        album_file_regex,
        single_regex,
        various_artists_regex,
        various_artists_file_regex,
    ):
        self.store = store
        self.album_regex = re.compile(album_regex)
        self.album_file_regex = re.compile(album_file_regex)
        self.single_regex = re.compile(single_regex)
        self.various_artists_regex = re.compile(various_artists_regex)
        self.various_artists_file_regex = re.compile(various_artists_file_regex)

    def match_store(self, path, source):
        filename = path.split(os.path.sep)[-1]
        # check for Various Artists - not enabled for all stores yet
        if self.store == "bandcamp":
            if source == "various_artists" and self.various_artists_regex.search(
                filename
            ):
                print("Match on various artists album for %s" % self.store)
                return True

        if source == "album" and self.album_regex.search(filename):
            print("Match on album for %s" % self.store)
            return True
        elif source == "single" and self.single_regex.match(filename):
            print("Match on single for %s" % self.store)
            return True
        else:
            return False

    def get_field(self, path, field, regex_type):
        if regex_type == "album":
            regex = self.album_regex
        elif regex_type == "album_file":
            regex = self.album_file_regex
        elif regex_type == "various_artists":
            regex = self.various_artists_regex
        elif regex_type == "various_artists_file":
            regex = self.various_artists_file_regex
        elif regex_type == "single":
            regex = self.single_regex
        else:
            err = "regex must be album, album_file, various_artists, various_artists_file, or single!"
            raise TypeError(err)

        filename = path.split(os.path.sep)[-1]
        try:
            if self.store == "juno download":
                # Deal with replacing things.  Eventually we'll generalize this.
                res = regex.match(filename).group(field)
                res = res.replace("_", " ").strip()
            elif self.store == "beatport":
                res = regex.match(filename).group(field)
                if field == "title":
                    if "Original Mix" in res:
                        res = res.replace("Original Mix", "").strip()

                return res
            else:
                return regex.match(filename).group(field)
        except (AttributeError, IndexError):
            if field == "track_number" and (
                path.endswith(".jpg") or path.endswith(".pdf")
            ):
                return "999"
            else:
                print(
                    "---- No data in %s for %s.  Please enter the correct string ----"
                    % (path, field)
                )
                r = input()
                return r.strip()


def build_parsers():
    parsers = []

    # Parser order matters here, I should improve this
    # name, album_regex, album_file_regex,
    # single_regex, various_artists_regex, various_artists_file_regex
    data = [
        # www.amazon.com, needs to be first because of the AMAZON prepend
        (
            "amazon",
            r"AMAZON (?P<artist>.+?) - (?P<album_title>.+)",
            r"(?P<track_number>\d\d) - (?P<title>.+?)\.(?P<extension>.+)",
            r"AMAZON (?P<artist>.+?) - (\d+?) - (?P<title>.+?)\.(?P<extension>.+)",
            "NO EXAMPLES YET",
            "NO EXAMPLES YET",
        ),
        # New amazon singles format!
        (
            "amazon - new singles",
            r"NO EXAMPLES YET",
            r"NO EXAMPLES YET",
            r"(\d\d?) - (?P<title>.+?)\.(?P<extension>.+)",
            "NO EXAMPLES YET",
            "NO EXAMPLES YET",
        ),
        # www.beatport.com
        (
            "beatport",
            r"NO EXAMPLES YET",
            r"NO EXAMPLES YET",
            r"(?P<artist>.+?) - (?P<title>.+?) \[(?P<label>.+?)\]\.(?P<extension>.+)",
            "NO EXAMPLES YET",
            "NO EXAMPLES YET",
        ),
        # www.bleep.com
        (
            "bleep",
            r"(?P<artist>.+?) - (?P<album_title>.+?) - (?P<extension>.+)",
            r"(?P<album_title>.+?)-(?P<track_number>\d\d\d)-(?P<artist>.+?)-(?P<title>.+?)\.(?P<extension>.+)",
            r"(?P<album_title>.+?)-\d\d\d-(?P<artist>.+?)-(?P<title>.+?)\.(?P<extension>.+)",
            "NO EXAMPLES YET",
            "NO EXAMPLES YET",
        ),
        # www.bandcamp.com
        (
            "bandcamp",
            r"(?P<artist>.+?) - (?P<album_title>.+)",
            r"(?P<artist>.+?) - (?P<album_title>.+?) - (?P<track_number>\d\d) (?P<title>.+?)\.(?P<extension>.+)",
            r"(?P<artist>.+?) - (?P<title>.+?)\.(?P<extension>.+)",
            r"Various Artists - (?P<album_title>.+)",
            r"(?P<artist>.+?) - (?P<album_title>.+?) - (?P<track_number>\d\d) (?P<title>.+?)\.(?P<extension>.+)",
        ),
        # www.junodownload.com
        (
            "juno download",
            r"NO EXAMPLES YET",
            r"NO EXAMPLES YET",
            r"\d-(?P<artist>.+?)_-_(?P<title>.+?)\.(?P<extension>.+?)",
            "NO EXAMPLES YET",
            "NO EXAMPLES YET",
        ),
    ]
    for (
        name,
        album_regex,
        file_regex,
        single_regex,
        various_artists_regex,
        various_artists_file_regex,
    ) in data:
        p = Parser(
            name,
            album_regex,
            file_regex,
            single_regex,
            various_artists_regex,
            various_artists_file_regex,
        )
        parsers.append(p)

    return parsers
