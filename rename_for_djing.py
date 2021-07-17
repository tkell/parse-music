import argparse
import os
import re
from tag_utils import get_tags


"""
Script to rename album files, e.g. '01 - So Glad',
to single files, e.g. 'Floorplan - So Glad'.

Mostly used when taking Serato crates on the go
as flat folders!
"""

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Rename Files For Djing")
    parser.add_argument("--folder", type=str, help="Path to folder to rename files in")
    args = parser.parse_args()
    path = args.folder
    if path[-1] != "/":
        path = path + "/"

    for filename in os.listdir(path):
        if re.match(r"\d+ - .*", filename):
            _, file_extension = os.path.splitext(filename)
            filepath = path + filename
            artist, title = get_tags(filepath)
            if not artist or not title:
                print(filename, "PANIC!")
                continue
            new_filename = artist + " - " + title
            new_filepath = path + new_filename + file_extension
            print(filepath, new_filepath)
            os.rename(filepath, new_filepath)
