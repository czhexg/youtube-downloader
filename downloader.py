# External imports
from pytubefix import YouTube
from pytubefix.cli import on_progress
from pytubefix.helpers import safe_filename
import ffmpeg

# Standard library imports
import os
import time
import threading

# Local imports
from content import Content, Video, Audio, CombinedContent
from constants import ContentType
from processor import ContentProcessor


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
        self.processor = ContentProcessor(
            self.video_path, self.audio_path, self.combined_path
        )
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

    def download_video(
        self,
        filename: str = None,
        result_container: dict[ContentType, Content] = {
            ContentType.VIDEO: None,
            ContentType.AUDIO: None,
        },
    ) -> Video:
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

                downloaded_video = Video(
                    title=self.title,
                    description=self.yt.description,
                    creator=self.yt.author,
                    duration=self.yt.length,
                    filename=filename,
                    filepath=os.path.join(self.video_path, filename),
                    thumbnail=self.yt.thumbnail_url,
                    resolution=video_stream.resolution,
                )
                result_container[ContentType.VIDEO] = downloaded_video
                return downloaded_video

            except Exception as e:
                print(f"Failed to download video: {e}")
        else:
            print("No video stream found.")

    def download_audio(
        self,
        filename: str = None,
        result_container: dict[ContentType, Content] = {
            ContentType.VIDEO: None,
            ContentType.AUDIO: None,
        },
    ) -> Audio:
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

                downloaded_audio = Audio(
                    title=self.title,
                    description=self.yt.description,
                    creator=self.yt.author,
                    duration=self.yt.length,
                    filename=filename,
                    filepath=os.path.join(self.audio_path, filename),
                    thumbnail=self.yt.thumbnail_url,
                    bitrate=audio_stream.abr,
                )
                result_container[ContentType.AUDIO] = downloaded_audio
                return downloaded_audio

            except Exception as e:
                print(f"Failed to download audio: {e}")
        else:
            print("No audio stream found.")

    def download_both(self) -> dict:
        """Downloads both video and audio using threading"""
        result_container: dict[ContentType, Content] = {
            ContentType.VIDEO: None,
            ContentType.AUDIO: None,
        }
        video_thread = threading.Thread(
            target=self.download_video, kwargs={"result_container": result_container}
        )
        audio_thread = threading.Thread(
            target=self.download_audio, kwargs={"result_container": result_container}
        )

        # Start threads
        video_thread.start()
        audio_thread.start()

        # Wait for both threads to complete
        video_thread.join()
        audio_thread.join()

        return result_container

    def handle_download(
        self, choice: str, to_split: bool = False, chunk_duration: int = 0
    ):
        """Handles the user's download choice. If combined is chosen and to_split is True, the content will be split into chunks before combining."""
        downloaded_content: dict[ContentType, Content] = {
            ContentType.VIDEO: None,
            ContentType.AUDIO: None,
        }
        if choice == "v":
            downloaded_content[ContentType.VIDEO] = self.download_video()
        elif choice == "a":
            downloaded_content[ContentType.AUDIO] = self.download_audio()
        elif choice == "b" or choice == "c":
            downloaded_content = self.download_both()
        else:
            print("Invalid choice. Exiting.")
            return

        if to_split:
            # check if chunk_duration is greater than the video duration
            if chunk_duration > self.yt.length:
                print(
                    "Chunk duration is greater than video duration. Content will not be split."
                )
            else:
                # split the video and audio files into chunks if the content is not None
                if downloaded_content[ContentType.VIDEO]:
                    video_chunks = self.processor.split_content(
                        chunk_duration, downloaded_content[ContentType.VIDEO]
                    )
                if downloaded_content[ContentType.AUDIO]:
                    audio_chunks = self.processor.split_content(
                        chunk_duration, downloaded_content[ContentType.AUDIO]
                    )

        if choice == "c":
            if to_split:
                # todo: loop through all the files returned after splitting and combine the video chunk with the corresponding audio chunk
                i = 0
                for video_chunk, audio_chunk in zip(video_chunks, audio_chunks):
                    self.processor.combine_audio_video(
                        video_chunk,
                        audio_chunk,
                        f"{video_chunk.title}_combined{i:03d}.mp4",
                    )
                    i += 1
            else:
                self.processor.combine_audio_video(
                    downloaded_content[ContentType.VIDEO],
                    downloaded_content[ContentType.AUDIO],
                    f"{self.title}_combined.mp4",
                )
