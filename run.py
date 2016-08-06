#!/usr/bin/env python
# encoding: utf=8

"""
Main file that runs both parsing processes
"""

from parse_singles import run_singles
from parse_albums import parse_albums

if __name__ == '__main__':
    run_singles('/home/thor/Desktop/unparsed')
    parse_albums('/home/thor/Desktop/unparsed')
