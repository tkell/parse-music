#!/usr/bin/env python
# encoding: utf=8

## singles are Artist - Title (Remix) [Label]

import os
import re

from utils import do_work
from utils import parse_file
from tag_utils import get_tags

from parser import build_parsers
from parser import select_parser

def parse_singles(filenames, folder_path, parsers):
    results = []
    for filename in file_names:
        if '.mp3' in filename or '.flac' in filename:
            # pick parser
            the_parser = None
            for parser in parsers:
                if parser.match_store(filename, source='file'):
                    the_parser = parser
                    break
            if the_parser == None:
                # panic!
                pass

            filepath = os.path.join(folder_path, filename)
            results.append((filepath, the_parser))

    return results

def parse_singles():
    parsers = build_parsers() # make the objects that pick the store, do lots of other things

    current_dir = os.getcwd()
    singles_path = os.path.join(current_dir, singles)
    singles = os.listdir(singles_path)
    results = parse_singles(singles, singles_path, parsers) # make a list of things to do

    tasks = []
    for path, parser in results:
        task = parse_file(filepath, parser)
    success = do_work(tasks) # rename or re-tag the files, as needed.
        `
