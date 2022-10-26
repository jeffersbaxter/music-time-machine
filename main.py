import os

import requests
from bs4 import BeautifulSoup

import spotipy
from spotipy.oauth2 import SpotifyOAuth

SPOTIFY_ID = os.environ.get("SPOTIFY_CLIENT_ID")
SPOTIFY_SECRET = os.environ.get("SPOTIFY_CLIENT_SECRET")
SPOTIFY_REDIRECT = os.environ.get("SPOTIPY_REDIRECT_URI")
BILLBOARD_URL = os.environ.get("BILLBOARD_TOP_100_URL")

time_destination = input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD:\n")

URL = f"{BILLBOARD_URL}{time_destination}"

response = requests.get(url=URL)
response.raise_for_status()

soup = BeautifulSoup(response.text, "html.parser")

chart_results_list = soup.find(name="div", class_="chart-results-list")

songs = [band.find(name="h3", class_="c-title").getText().strip() for band in chart_results_list.find_all(name="div", class_="o-chart-results-list-row-container")]

auth_manager = SpotifyOAuth(
    client_id=SPOTIFY_ID,
    client_secret=SPOTIFY_SECRET,
    redirect_uri=SPOTIFY_REDIRECT,
    show_dialog=True,
    cache_path="token.txt",
    scope="playlist-modify-public"
)
spotify = spotipy.Spotify(auth_manager=auth_manager)

user_id = spotify.current_user()["id"]

song_uris = []
year = time_destination.split("-")[0]
for song in songs:
    result = spotify.search(q=f"track:{song} year:{year}")
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")

playlist = spotify.user_playlist_create(
    user=user_id,
    name=f"{time_destination} Billboard 100",
    public=True
)

spotify.playlist_add_items(
    playlist_id=playlist["id"],
    items=song_uris
)
