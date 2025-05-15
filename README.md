# VidLii Downloader
This is a simple Python script that downloads videos from [VidLii](https://www.vidlii.com/), a video sharing site reminiscent of old YouTube. I'm aiming for compatibility with both Windows and Linux. There is no reason I can think of for it not to work on Mac or other OSes such as BSD, but it isn't guarenteed.

Accepts VidLii links from the command line or from stdin. E.g. "python3 downloader.py https://vidlii.com/watch?v=..." will work. I have made an effort to avoid any possible issues with filenames on Windows and Linux. Videos will generally be named after their title on the site, otherwise they will be named video1.mp4, video2.mp4, and so on. Also, the script's user agent string makes it clear that it is a script, not an actual browser, and even links back to this repository. Note that I am not responsible for nor do I condone any malicious usage of this script.

Developed and tested on Python 3.11.2, will likely work on many if not all versions of Python 3.
