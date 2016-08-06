#!/usr/bin/env python
# encoding: utf=8

## singles are Artist - Title (Remix) [Label]

import os
import re

from utils import do_work
from utils import parse_file
from tag_utils import get_tags

from parser import build_parsers

def parse_singles(filenames, folder_path, parsers):
    results = []
    for filename in filenames:
        if '.mp3' in filename.lower() or '.flac' in filename.lower():
            # pick parser
            the_parser = None
            for parser in parsers:
                if parser.match_store(filename, source='file'):
                    the_parser = parser
                    break
            if the_parser == None:
                # panic!
                print "NO PARSER FOUND WHAT"
                pass

            filepath = os.path.join(folder_path, filename)
            results.append((filepath, the_parser))

    return results

def run_singles(starting_folder):
    parsers = build_parsers() # make the objects that pick the store, do lots of other things
    singles_path = starting_folder + os.path.sep + 'singles'
    singles = os.listdir(singles_path)
    results = parse_singles(singles, singles_path, parsers) # make a list of things to do
    
    tasks = []
    context = 'single'
    for filepath, parser in results:
        task = parse_file(filepath, parser, context)
        tasks.extend(task)

    success = do_work(tasks) # rename or re-tag the files, as needed.
