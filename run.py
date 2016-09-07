#!/usr/bin/env python
# encoding: utf=8

"""
Main file that runs both parsing processes
"""

from parse_singles import parse_singles
from parse_albums import parse_albums

if __name__ == '__main__':
    parse_singles('/Users/thor/Desktop/unparsed/singles', '/home/thor/Desktop/parsed')
    parse_albums('/Users/thor/Desktop/unparsed', '/home/thor/Desktop/parsed')
