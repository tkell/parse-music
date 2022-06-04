import argparse
import os
import re
import urllib.parse
from collections import defaultdict

import requests
import pyperclip

label_regex = r"[(.*)]"
singles_path = "/Volumes/Music/Singles/"
with open("discogs-token.txt") as f:
    discogs_token = f.readline().strip()


def search_discogs(artist, track, label):
    a = urllib.parse.quote(artist.lower())
    t = urllib.parse.quote(track.lower())
    l = urllib.parse.quote(label.lower())
    url = f"https://api.discogs.com/database/search?artist={a}&label={l}&track={t}"
    return call_discogs_no_cache(url)


def call_discogs_no_cache(url):
    headers = {
        "user-agent": "DiscogsOrganize +http://tide-pool.ca",
        "Authorization": f"Discogs token={discogs_token}",
    }
    r = requests.get(url, headers=headers)

    print("calling: ", url)
    try:
        result = r.json()
    except json.JSONDecodeError:
        print("calling url failed:", url)
        print("response reason", r.reason, r.status_code)

    return result


def is_music_file(filename):
    return filename.endswith(".mp3") or filename.endswith(".flac")


def starts_with(filename, letter):
    return filename.lower().startswith(letter.lower())


def enter_data_manually():
    print("Enter the track number for this track")
    track_number = input().strip()

    print("Enter the discogs url for this release")
    discogs_url = input().strip()
    return track_number, discogs_url


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--starting_letter", type=str, required=True)
    args = parser.parse_args()

    singles = os.listdir(singles_path)
    artist_and_label_groups = defaultdict(list)
    for single in singles:
        if starts_with(single, args.starting_letter) and is_music_file(single):
            artist = single.split(" - ")[0]
            label = re.search(r"\[(.+?)\]", single).group(1)
            key = (artist, label)
            artist_and_label_groups[key].append(single)

    for key, matched_singles in artist_and_label_groups.items():
        artist, label = key
        # This case is "easy":  we just move the one file
        # we need to know
        #  - what is the track number for this track?
        #  - what is the discogs url for this release?
        if len(matched_singles) == 1:
            filename = matched_singles[0]

            msg = "'s' to skip, 'd' for discogs search, 'e' to enter data manually"
            print(msg)
            print(filename)

            action = input().strip().lower()
            if action == "s":
                next
            elif action == "q":
                break
            elif action == "d":
                track = filename.split(" - ")[1].split(" [")[0]
                res = search_discogs(artist, track, label)
                print(res)
            elif action == "e":
                track_number, discogs_url = enter_data_manually()
