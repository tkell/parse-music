#!/usr/bin/env python
# encoding: utf=8

import os
from mock import MagicMock
from mock import call

from utils import check_various_artists
from utils import check_filetype
from utils import do_work

import tag_utils


def test_check_various_artists():
    reg_path = '/home/wombat/music/An Artist - A Title'
    various_path = '/home/wombat/music/Various Artists - A Title'

    assert(check_various_artists(reg_path) == False)
    assert(check_various_artists(various_path) == True)

def test_check_filetype():
    mp3_path = '/home/wombat/music/An Artist - A Title.mp3'
    flac_path = '/home/wombat/music/Various Artists - A Title.flac'
    none_path = '/home/wombat/music/Various Artists - A Title'

    assert(check_filetype(mp3_path) == 'mp3')
    assert(check_filetype(flac_path) == 'flac')
    assert(check_filetype(none_path) == None)

def test_do_work_rename():
    rename_tasks = [('rename', 'old_path', 'new_path')]
    os.rename = MagicMock()
    do_work(rename_tasks)
    os.rename.assert_called_with('old_path', 'new_path')

def test_do_work_retag():
    retag_tasks = [('retag', 'path', 'the_artist', 'the_title')]
    tag_utils.set_tag = MagicMock()
    try:
        do_work(retag_tasks)
    except OSError:
        pass
    c1 = call('path', 'artist', 'the_artist')
    c2 = call('path', 'title', 'the_title')
    tag_utils.set_tag.assert_has_calls(c1, c2)
