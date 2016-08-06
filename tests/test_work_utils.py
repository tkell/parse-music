#!/usr/bin/env python
# encoding: utf=8

import os
from mock import MagicMock
from mock import call

from work_utils import do_work

import tag_utils

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
    tag_utils.set_tag.assert_has_calls([c1, c2])

