#!/usr/bin/env python
# encoding: utf=8

"""
Main file that runs both parsing processes
"""
import argparse
from parse_singles import parse_singles
from parse_albums import parse_albums


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry_run", help="Dry run", action="store_true")
    args = parser.parse_args()
    if args.dry_run:
        print("Launching dry run, not doing work.")
    else:
        print("Launching regular run...")

    parse_singles(
        '/Users/thor/Desktop/unparsed/singles',
        '/Users/thor/Desktop/parsed/singles',
        args.dry_run,
    )
    parse_albums(
        '/Users/thor/Desktop/unparsed',
        '/Users/thor/Desktop/parsed/albums',
        args.dry_run,
    )
