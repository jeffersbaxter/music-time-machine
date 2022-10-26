import os

import requests
from bs4 import BeautifulSoup

SPOTIFY_CLIENT_ID = os.environ.get("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.environ.get("SPOTIFY_CLIENT_SECRET")

time_destination = input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD:\n")

URL = f"https://www.billboard.com/charts/hot-100/{time_destination}"

response = requests.get(url=URL)
response.raise_for_status()

soup = BeautifulSoup(response.text, "html.parser")

chart_results_list = soup.find(name="div", class_="chart-results-list")

songs = [band.find(name="h3", class_="c-title").getText().strip() for band in chart_results_list.find_all(name="div", class_="o-chart-results-list-row-container")]
print(songs[:10])


