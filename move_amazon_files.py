## Deals with amazon's stupid directories, prepends them with AMAZON
## This has been tweaked to only work for singles!
## You'll need to hack it to work for albums, somehow.

import os
import shutil

def run_amazon(path):
    files = os.listdir(path)
    amazon_dirs = [f for f in files if 'Amazon-Music-Download' in f]
    for amazon_dir in amazon_dirs:
        potential_files = os.walk(path + os.path.sep + amazon_dir)
        for path_tuple in potential_files:
            filepath = path_tuple[0]
            if path_tuple[-1]:
                filename = path_tuple[-1][0]
                if '.mp3' in filename or '.flac' in filename:
                    artist = path_tuple[0].split(os.path.sep)[-2]
                    new_filename = 'AMAZON ' + artist + " - " + filename
                    shutil.move(filepath + os.path.sep + filename, path + os.path.sep + new_filename)

run_amazon('/Users/thor/Desktop/unparsed/singles')

