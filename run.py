#!/usr/bin/env python
# encoding: utf=8

"""
Main file that runs both parsing processes
"""

from parse_singles import parse_singles
from parse_albums import parse_albums

if __name__ == 'main':
    parse_singles()
    parse_albums()
