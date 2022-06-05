import argparse
import os
import random
import re
import urllib.parse
from collections import defaultdict

import requests
import pyperclip

## SETUP AND CONSTANTS
label_regex = r"[(.*)]"
singles_path = "/Volumes/Music/Singles/"
with open("discogs-token.txt") as f:
    discogs_token = f.readline().strip()


class SkipRelease(Exception):
    pass


class StopRelease(Exception):
    pass


## DISCOGS API
def search_discogs(artist, track, label):

    a = urllib.parse.quote(artist.lower())
    # Remove beatport's habit of "original mix"
    t = urllib.parse.quote(track.lower().replace("(original mix)", ""))
    l = urllib.parse.quote(label.lower())
    url = f"https://api.discogs.com/database/search?artist={a}&label={l}&track={t}"
    discogs_json = call_discogs_no_cache(url)

    if len(discogs_json["results"]) == 0:
        url = f"https://api.discogs.com/database/search?artist={a}&track={t}"
        discogs_json = call_discogs_no_cache(url)

    if len(discogs_json["results"]) == 0:
        url = f"https://api.discogs.com/database/search?artist={a}"
        discogs_json = call_discogs_no_cache(url)

    if len(discogs_json["results"]) == 0:
        url = f"https://api.discogs.com/database/search?track={t}"
        discogs_json = call_discogs_no_cache(url)

    return discogs_json


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


## DISCOGS DATA
def print_discogs_releases(index, release):
    label = release.get("label", "label missing")
    catno = release.get("catno", "catno missing")
    title = release.get("title", "title missing")
    year = release.get("year", "year missing")
    print(f"{index}: {title} - {label} {catno} {year}")


## BIG UX FUNCTIONS
def prompt(msg, klass=str):
    char = random.choice(["-", "_", "~", ">", "*"])
    print(char * 4 + " " + msg)
    return klass(input().strip())


def parse_releases_from_discogs(discogs_json):
    if len(discogs_json["results"]) == 0:
        print("no release found!!")
        return None

    print("Found releases:")
    for index, release in enumerate(discogs_json["results"]):
        print_discogs_releases(index, release)

    release_number = prompt("Select a release", int)
    release = discogs_json["results"][release_number]
    release_url = release["resource_url"]
    release_details = call_discogs_no_cache(release_url)

    for index, track in enumerate(release_details["tracklist"]):
        print(f"{index}, {track}")

    track_number = prompt("Enter the index for this track / press 'x' to go back", int)
    if track_number == "x":
        # panic / return from whence we came / re-run parse_release?
        pass

    track_number = int(track_number)
    tracklist = [track["title"] for track in release_details["tracklist"]]
    discogs_url = release_details["uri"]
    release_title = release_details["title"]
    return release_title, track_number, tracklist, discogs_url


def enter_data_manually(track):
    release_title = prompt("Enter the title for this release")
    discogs_url = prompt("Enter the discogs url for this release")
    num_tracks = prompt("How many tracks do we have?")
    track_number = prompt("Enter the track number for this track")

    tracklist = []
    for i in range(0, num_tracks - 1):
        if i != track_number:
            track_title = prompt(f"Enter the track title for track {i}")
            tracklist.append(track_title)
    # insert our track!
    tracklist.insert(track_number - 1, track)

    return release_title, track_number, tracklist, discogs_url


def interact_and_get_data(artist, track, label):
    print(f"{artist} - {track} [{label}]")
    action = prompt("'s' to skip, 'd' for discogs search, 'e' to enter data manually")
    if action == "s":
        raise SkipRelease
    elif action == "q":
        raise StopRelease
    elif action == "d":

        ## so this is tricky, we need to do a bunch of searches
        ## if we get an empty search result, do the next search
        ## if we get a search result, we don't want, we want to be able to skip that search manually

        ## also! once we've selected a release, if it is bad, we want to be able to go back to the previous list
        ## and we want to be able to move to "manual entry" if we don't like any of the searches
        res = search_discogs(artist, track, label)
        return parse_releases_from_discogs(res)

    elif action == "e":
        return enter_data_manually(track)


def group_by_artist_and_label(singles):
    def is_music_file(filename):
        return filename.endswith(".mp3") or filename.endswith(".flac")

    def starts_with(filename, letter):
        return filename.lower().startswith(letter.lower())

    def key_by_artist_and_label(single):
        artist = single.split(" - ")[0]
        label = re.search(r"\[(.+?)\]", single).group(1)
        return (artist, label)

    artist_and_label_groups = defaultdict(list)
    for single in singles:
        if starts_with(single, args.starting_letter) and is_music_file(single):
            key = key_by_artist_and_label(single)
            artist_and_label_groups[key].append(single)
    return artist_and_label_groups


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--starting_letter", type=str, required=True)
    args = parser.parse_args()

    singles = os.listdir(singles_path)
    artist_and_label_groups = group_by_artist_and_label(singles)

    # This case is "easy":  we just move the one file
    results = []
    for key, matched_singles in artist_and_label_groups.items():
        if len(matched_singles) == 1:
            artist, label = key
            filename = matched_singles[0]
            track = filename.split(" - ")[1].split(" [")[0]
            try:
                result = interact_and_get_data(artist, track, label)
                if result:
                    results.append(result)
            except SkipRelease:
                next
            except StopRelease:
                break

    # hey, now do something with release_title, track_number, tracklist, and discogs_url!
    # specifially:
    # make a new folder called release_title
    # move filename in there, named "01 - track", based on track_number
    # for the other tracks, make "02 - track.marker"
    # make a discogs_url.txt file, and write the url to it
