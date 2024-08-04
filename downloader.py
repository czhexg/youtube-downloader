from pytubefix import YouTube
from pytubefix.cli import on_progress
from pytubefix.helpers import safe_filename
import os


class YouTubeDownloader:
    def __init__(self, url):
        self.url = url
        self.yt = YouTube(url, on_progress_callback=on_progress)
        self.title = safe_filename(self.yt.title, max_length=240)
        self.base_path = os.path.join(os.getcwd(), "youtube_vids")
        self.video_path = os.path.join(self.base_path, "video")
        self.audio_path = os.path.join(self.base_path, "audio")
        self.combined_path = os.path.join(self.base_path, "combined")
        self._create_directories()

    def _create_directories(self):
        os.makedirs(self.video_path, exist_ok=True)
        os.makedirs(self.audio_path, exist_ok=True)
        os.makedirs(self.combined_path, exist_ok=True)
