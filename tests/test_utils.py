#!/usr/bin/env python
# encoding: utf=8

from utils import check_various_artists
from utils import check_filetype


def test_check_various_artists():
    reg_path = "/home/wombat/music/An Artist - A Title"
    various_path = "/home/wombat/music/Various Artists - A Title"

    assert check_various_artists(reg_path) is False
    assert check_various_artists(various_path) is True


def test_check_filetype():
    mp3_path = "/home/wombat/music/An Artist - A Title.mp3"
    flac_path = "/home/wombat/music/Various Artists - A Title.flac"
    none_path = "/home/wombat/music/Various Artists - A Title"

    assert check_filetype(mp3_path) == "mp3"
    assert check_filetype(flac_path) == "flac"
    assert check_filetype(none_path) is None
