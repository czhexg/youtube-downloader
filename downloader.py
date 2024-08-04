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

    def download_video(self, filename=None):
        """Downloads the highest resolution video stream with avc1 codec"""
        if not filename:
            filename = f"{self.title}_video.mp4"
        video_stream = (
            self.yt.streams.filter(
                progressive=False,
                file_extension="mp4",
                only_video=True,
                custom_filter_functions=[lambda s: s.video_codec.startswith("avc1")],
            )
            .order_by("resolution")
            .desc()
            .first()
        )
        if video_stream:
            video_stream.download(output_path=self.video_path, filename=filename)
            print(
                f"Video downloaded successfully: {os.path.join(self.video_path, filename)}"
            )
        else:
            print("No video stream found.")

    def download_audio(self, filename=None):
        """Downloads the highest quality audio stream"""
        if not filename:
            filename = f"{self.title}_audio.mp3"
        audio_stream = (
            self.yt.streams.filter(
                progressive=False, file_extension="mp4", only_audio=True
            )
            .order_by("abr")
            .desc()
            .first()
        )
        if audio_stream:
            audio_stream.download(output_path=self.audio_path, filename=filename)
            print(
                f"Audio downloaded successfully: {os.path.join(self.audio_path, filename)}"
            )
        else:
            print("No audio stream found.")
