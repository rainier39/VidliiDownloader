# ------------------------------------------------------------------ #
# VidLii downloader. Downloads videos off of VidLii given their URL. #
# ------------------------------------------------------------------ #

import requests
from bs4 import BeautifulSoup
import os
import sys

version = "1.1"

# We have to send the site a user agent.
headers = {"User-Agent": "Mozilla/5.0 +https://github.com/rainier39/VidliiDownloader VidLiiDownloader/" + version}

# List of characters that can't be used in the filename (for Windows compatibility).
badchars = ["<", ">", ":", "\"", "/", "\\", "|", "?", "*"]

# List of Windows reserved filenames.
badfilenames = ["con", "prn", "aux", "nul", "com1", "com2", "com3", "com4", "com5", "com6", "com7", "com8", "com9", "com0", "lpt1", "lpt2", "lpt3", "lpt4", "lpt5", "lpt6", "lpt7", "lpt8", "lpt9", "lpt0", "com¹", "com²", "com³", "lpt¹", "lpt²", "lpt³"]

def gracefulExit():
  # If we're on Windows, wait for user input so the window doesn't just close with no output from their perspective.
  if (sys.platform == "win32"):
    input("Press enter to exit: ")
  exit()

# Prompt the user for a VidLii URL if one wasn't supplied on the command line.
if (len(sys.argv) < 2):
  url = input("Please enter the URL of the VidLii video you wish to download: ")
else:
  url = sys.argv[1]

# Make sure that this is a valid VidLii URL.
if not url.startswith("https://www.vidlii.com/watch?v="):
  print("Error: supplied URL doesn't appear to be a valid VidLii video link.")
  gracefulExit()

# Get the page.
try:
  page = requests.get(url, headers=headers)
except:
  print("Error: failed to find video. Maybe VidLii is down or you don't have a working internet connection.")
  gracefulExit()

# TODO: more error handling for VidLii being down, the video not existing, etc.

# Invoke BeautifulSoup.
soup = BeautifulSoup(page.content, "lxml")

# Get the path to the video file itself.
filepath = (soup.find('video'))["src"]

# We also grab the title for the filename.
title = soup.find('h1').text

# Remove any forbidden characters from the filename.
for c in badchars:
  title = title.replace(c, "")

# On Windows, filenames aren't supposed to end with a period. Also, this takes care of the reserved "." and ".." Linux filenames.
while (title.endswith(".")):
  title = title[:-1]

# Stop the title from being a reserved filename (on Windows and Linux).
if (title.lower() in badfilenames):
  print("Warning: video title was a reserved filename, changing it to something else.")
  title = ""

# On Windows, something like "nul.txt" is just as bad as "nul" so stop those as well.
for bad in badfilenames:
  if (title.lower().startswith(bad + ".")):
    print("Warning: video title was a reserved filename, changing it to something else.")
    title = ""

# If we have a blank title for any reason, lets not.
cwd = os.getcwd()
if (title == ""):
  for i in range(1,65536):
    if not os.path.exists(os.path.join(cwd, "video" + str(i) + ".mp4")):
      title = "video" + str(i)
      break

# If someone has downloaded that many titleless videos, it's over.
if (title == ""):
  print("Error: ran out of names for video.")
  gracefulExit()

# Make sure that a video with this title doesn't already exist.
if os.path.exists(os.path.join(cwd, title + ".mp4")):
  choice = input("Notice: a video with that name already exists. Overwrite? (y/n): ")
  if not (choice.lower() == "y"):
    gracefulExit()

# Get the video file.
print("Downloading " + title + "...")
video = requests.get("https://www.vidlii.com" + filepath, headers=headers)

# Write the video file to the disk.
f = open(title + ".mp4", "wb")
f.write(video.content)
f.close()

# Send some output when we're finished.
print("Done! Successfully downloaded " + title + ".mp4!")

gracefulExit()
