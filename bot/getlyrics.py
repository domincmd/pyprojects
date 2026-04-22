import spotipy
from spotipy.oauth2 import SpotifyOAuth
import random
import requests

MUSIC_ALIASES = {
    "Goddamn": "Goddamn (feat. Biffe)"
}

def pick_snippet(lyrics, min_lines=4, max_lines=7):
    lines = [l.strip() for l in lyrics.split("\n") if l.strip()]
    
    if len(lines) <= min_lines:
        return "\n".join(lines)
    
    size = random.randint(min_lines, max_lines)
    start = random.randint(0, max(0, len(lines) - size))
    
    return "\n".join(lines[start:start+size])

def get_lyrics(song, artist):
        url = f"https://api.lyrics.ovh/v1/{artist}/{song}"
        r = requests.get(url)

        if r.status_code == 200:
            data = r.json()
            return data.get("lyrics")
        return None

def get_tracks_array():
    client_id = "4994c5f48c11423d801cd206a0887d86"
    client_secret = "e474e98dfd7440acac49b616a24a903d"

    sp = spotipy.Spotify(
        auth_manager=SpotifyOAuth(
            client_id=client_id,
            client_secret=client_secret,
            redirect_uri="http://127.0.0.1:8888/callback",
            scope="playlist-read-private"
        )
    )

    playlist_id = "1S09xfd2sdYzALJb9K6SVj"

    results = sp.playlist_items(playlist_id)

    tracks = []

    for item in results["items"]:
        track = item.get("item")

        if not track:
            continue

        song = track["name"]
        artist = track["artists"][0]["name"]

        song = song.split(" - ")[0]

        if song in MUSIC_ALIASES:
            song = MUSIC_ALIASES[song]

        tracks.append([song, artist])
    
    return tracks

def get_random_lyric():
    tracks = get_tracks_array()

    song, artist = random.choice(tracks)

    lyrics = get_lyrics(song, artist)

    while lyrics == None:
        song, artist = random.choice(tracks)

        lyrics = get_lyrics(song, artist)

    lyrics = lyrics.lower().replace("'", "").replace("’", "")

    #lyrics_array = lyrics.split("\n\n")

    lyrics = pick_snippet(lyrics)

    return lyrics

