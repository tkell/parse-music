## Deals with amazon's stupid directories, prepends them with AMAZON

import os
import shutil

def run_amazon(path):
    files = os.listdir(path)
    amazon_dirs = [f for f in files if 'Amazon-Music-Download' in f]
    for amazon_dir in amazon_dirs:
        potential_files = os.walk(path + os.path.sep + amazon_dir)
        for path_tuple in potential_files:
            filepath  = path_tuple[0]
            if path_tuple[-1]:
                filename = path_tuple[-1][0]
                if '.mp3' in filename or '.flac' in filename:
                    shutil.move(filepath + os.path.sep + filename, path + os.path.sep + 'AMAZON ' + filename)

run_amazon('/Users/thor/Desktop/unparsed/singles')

