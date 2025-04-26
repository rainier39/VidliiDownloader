# ------------------------------------------------------------------ #
# Vidlii downloader. Downloads videos off of Vidlii given their URL. #
# ------------------------------------------------------------------ #

import requests
from bs4 import BeautifulSoup

# We have to send the site a user agent.
headers = {"User-Agent": "Mozilla/5.0 Vidlii Downloader"}

# List of characters that can't be used in the filename (for Windows compatibility).
badchars = ["<", ">", ":", "\"", "/", "\\", "|", "?", "*"]

# Prompt the user for a Vidlii URL.
url = input("Please enter the URL of the Vidlii video you wish to download: ")

# Get the page.
page = requests.get(url, headers=headers)

# TODO: error handling for Vidlii being down, the video not existing, etc.

# Invoke BeautifulSoup.
soup = BeautifulSoup(page.content, "lxml")

# Get the path to the video file itself.
filepath = (soup.find('video'))["src"]

# We also grab the title for the filename.
title = soup.find('h1').text

# Remove any forbidden characters from the filename.
for c in badchars:
  title = title.replace(c, "")

# TODO: stop the title from being a reserved filename (on Windows and Linux).

# TODO: have a scheme for setting the title if it's blank, change the title if a file with that name already exists (e.g. video.mp4 exists, so we make the title video1, and so forth).

# Get the video file.
video = requests.get("https://www.vidlii.com" + filepath, headers=headers)

# Write the video file to the disk.
f = open(title + ".mp4", "wb")
f.write(video.content)
f.close()

# Send some output when we're finished.
print("Done! Successfully downloaded " + title + ".mp4!")

# TODO: if we're on Windows, wait for user input so the window doesn't just close with no output from their perspective.
