import argparse
import os
import random
import re
import shutil
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


class DiscogsSearchFailed(Exception):
    pass


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


def prompt(msg, klass=str):
    char = random.choice(["-", "_", "~", ">", "*"])
    print(char * 4 + " " + msg)
    return klass(input().strip())


def interact_and_get_data(artist, track, label):
    def enter_data_manually(track):
        release_title = prompt("Enter the title for this release")
        discogs_url = prompt("Enter the discogs url for this release")
        num_tracks = prompt("How many tracks do we have?", int)
        track_number = prompt("Enter the track index for this track", int)

        return release_title, track_number, num_tracks, discogs_url

    def parse_releases_from_discogs(discogs_json):
        release_number = prompt("Select a release", int)
        release = discogs_json["results"][release_number]
        release_url = release["resource_url"]
        release_details = call_discogs_no_cache(release_url)

        for index, track in enumerate(release_details["tracklist"]):
            print(f"{index}, {track}")

        track_number = prompt("Enter the index for this track / '-1' to go back", int)
        if track_number == -1:
            # this is our "we did not like this release" state!
            return None

        track_number = int(track_number)
        num_tracks = len(release_details["tracklist"])
        discogs_url = release_details["uri"]
        release_title = release_details["title"]
        return release_title, track_number, num_tracks, discogs_url

    def print_discogs_releases(index, release):
        label = release.get("label", "label missing")
        catno = release.get("catno", "catno missing")
        title = release.get("title", "title missing")
        year = release.get("year", "year missing")
        print(f"{index}: {title} - {label} {catno} {year}")

    def search_discogs(artist, track, label, search_attempt):
        a = urllib.parse.quote(artist.lower())
        t = urllib.parse.quote(track.lower().replace("(original mix)", ""))
        l = urllib.parse.quote(label.lower())

        if search_attempt == 0:
            url = f"https://api.discogs.com/database/search?artist={a}&label={l}&track={t}"
        elif search_attempt == 1:
            url = f"https://api.discogs.com/database/search?artist={a}&track={t}"
        elif search_attempt == 2:
            url = f"https://api.discogs.com/database/search?artist={a}&label={l}"
        elif search_attempt == 3:
            url = f"https://api.discogs.com/database/search?track={t}&label={l}"
        elif search_attempt == 4:
            url = f"https://api.discogs.com/database/search?artist={a}"
        elif search_attempt == 5:
            url = f"https://api.discogs.com/database/search?track={t}"
        else:
            raise DiscogsSearchFailed

        discogs_json = call_discogs_no_cache(url)
        return discogs_json

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
        the_search_is_good = False
        discogs_json = None
        search_attempt = 0
        while not the_search_is_good:
            try:
                discogs_json = search_discogs(artist, track, label, search_attempt)
            except DiscogsSearchFailed:
                break

            if not discogs_json or len(discogs_json["results"]) == 0:
                search_attempt += 1
                continue
            else:
                print("Found releases from this search:")
                for index, release in enumerate(discogs_json["results"]):
                    print_discogs_releases(index, release)

            action = prompt("A good search? 'y' or 'n'?")
            if action == "y":
                the_search_is_good = True
            elif action == "n":
                search_attempt += 1

        if not discogs_json or the_search_is_good == False:
            ## and we want to be able to move to "manual entry" if we don't like any of the searches
            action = prompt("Fall back to manual entry, or skip?, 'e' or 's'?")
            if action == "e":
                return enter_data_manually(track)
            elif action == "s":
                raise SkipRelease

        results = parse_releases_from_discogs(discogs_json)
        while not results:
            print("Found releases from this search:")
            for index, release in enumerate(discogs_json["results"]):
                print_discogs_releases(index, release)
            results = parse_releases_from_discogs(discogs_json)

        return results

    elif action == "e":
        return enter_data_manually(track)


def group_by_artist_and_label(starting_letter, singles):
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
    artist_and_label_groups = group_by_artist_and_label(args.starting_letter, singles)

    # This case is "easy":  we just move the one file
    results = []
    for key, matched_singles in artist_and_label_groups.items():
        if len(matched_singles) == 1:
            artist, label = key
            filename = matched_singles[0]
            track = filename.split(" - ")[1].split(" [")[0]
            extension = filename.split(".")[-1]
            try:
                result = interact_and_get_data(artist, track, label)
                if result:
                    old_data = (filename, artist, track, label, extension)
                    results.append((result, old_data))
            except SkipRelease:
                next
            except StopRelease:
                break

    for new_data, old_data in results:
        release_title, track_number, num_tracks, discogs_url = new_data
        filename, artist, track, label, extension = old_data

        track_number = track_number + 1
        folder = f"{artist} - {release_title} [{label}]".replace("/", "--")
        new_filename = f"{track_number:02d} - {track}.{extension}"
        meta_filename = f"{num_tracks}.tracks"

        print(f"Preparing to move {filename}")
        print(f"New folder is {folder}")
        print(f"New track filename is {new_filename}")
        print(f"Would write the discogs url to {meta_filename}")
        albums_path = "/Volumes/Music/Albums/"
        action = prompt("Write, y / n?")

        if action == "y":
            folder_path = os.path.join(albums_path, folder)
            old_track_path = os.path.join(singles_path, filename)
            track_path = os.path.join(folder_path, new_filename)
            meta_path = os.path.join(folder_path, meta_filename)

            os.mkdir(folder_path)
            shutil.move(old_track_path, track_path)
            with open(meta_path, "w") as f:
                f.write(discogs_url)
            print("done writing, insert celebratory emojis here")
