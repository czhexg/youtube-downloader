from pytubefix import YouTube
from pytubefix.cli import on_progress
from pytubefix.helpers import safe_filename
import ffmpeg

import os
import time


class YouTubeDownloader:
    def __init__(self, url: str, retries: int = 3):
        self.url = url
        self.yt = YouTube(url, on_progress_callback=on_progress)
        self.title = safe_filename(self.yt.title, max_length=240)
        self.retries = retries
        self.base_path = os.path.join(os.getcwd(), "youtube_vids")
        self.video_path = os.path.join(self.base_path, "video")
        self.audio_path = os.path.join(self.base_path, "audio")
        self.combined_path = os.path.join(self.base_path, "combined")
        self._create_directories()

    def _create_directories(self):
        os.makedirs(self.video_path, exist_ok=True)
        os.makedirs(self.audio_path, exist_ok=True)
        os.makedirs(self.combined_path, exist_ok=True)

    def _download_with_retries(self, stream, output_path: str, filename: str) -> bool:
        attempts = 0
        while attempts < self.retries:
            try:
                stream.download(output_path=output_path, filename=filename)
                return True
            except Exception as e:
                attempts += 1
                print(f"Download failed: {e}. Retrying ({attempts}/{self.retries})...")
                time.sleep(1)
        raise Exception(f"Failed to download after {self.retries} attempts.")

    def download_video(self, filename: str = None) -> None:
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
            try:
                self._download_with_retries(video_stream, self.video_path, filename)
                print(
                    f"Video downloaded successfully: {os.path.join(self.video_path, filename)}"
                )
            except Exception as e:
                print(f"Failed to download video: {e}")
        else:
            print("No video stream found.")

    def download_audio(self, filename: str = None) -> None:
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
            try:
                self._download_with_retries(audio_stream, self.audio_path, filename)
                print(
                    f"Audio downloaded successfully: {os.path.join(self.audio_path, filename)}"
                )
            except Exception as e:
                print(f"Failed to download audio: {e}")
        else:
            print("No audio stream found.")

    def combine_audio_video(
        self, video_filename: str, audio_filename: str, output_filename: str
    ):
        video_path = os.path.join(self.video_path, video_filename)
        audio_path = os.path.join(self.audio_path, audio_filename)
        output_path = os.path.join(self.combined_path, output_filename)

        input_video = ffmpeg.input(video_path)
        input_audio = ffmpeg.input(audio_path)

        ffmpeg.concat(input_video, input_audio, v=1, a=1).output(output_path).run()
        print(f"Combined video saved to: {output_path}")
