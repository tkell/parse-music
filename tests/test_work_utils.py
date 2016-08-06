#!/usr/bin/env python
# encoding: utf=8

import os
from mock import MagicMock
from mock import call

from work_utils import do_work
from work_utils import select_work

import tag_utils

def test_do_work_rename():
    rename_tasks = [('rename', 'old_path', 'new_path')]
    os.rename = MagicMock()
    do_work(rename_tasks)
    os.rename.assert_called_with('old_path', 'new_path')

def test_do_work_retag():
    # Note that this implicity tests tag_utils
    retag_tasks = [('retag', 'path', 'the_artist', 'the_title')]
    tag_utils.set_tag = MagicMock()
    try:
        do_work(retag_tasks)
    except OSError:
        pass
    c1 = call('path', 'artist', 'the_artist')
    c2 = call('path', 'title', 'the_title')
    tag_utils.set_tag.assert_has_calls([c1, c2])


#select_work(filepath, tag_artist, tag_title, file_artist, file_title, new_name_from_file, new_name_from_tag)
def test_select_work_rename():
    res = select_work('path', 'artist', 'title', 'artist', 'title', 'new_file_name', 'new_tag_name')
    assert(res == [('rename', 'path', 'new_file_name')])

def test_select_work_tag_rename():
    res = select_work('path', 'artist', 'title', 'tag_artist', 'tag_title', 'new_file_name', 'new_tag_name')
    assert(res == [('rename', 'path', 'new_tag_name')])

def test_select_work_rename_and_move():
    res = select_work('path', None, None, 'artist', 'title', 'new_file_name', 'new_tag_name')
    print res
    assert(res == [('retag', 'path', 'artist', 'title'), ('rename', 'path', 'new_file_name')])
