from pytubefix import YouTube
from pytubefix.cli import on_progress
import os


class YouTubeDownloader:
    def __init__(self, url):
        self.url = url
        self.yt = YouTube(url, on_progress_callback=on_progress)
