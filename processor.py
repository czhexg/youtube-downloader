import ffmpeg

import os

from constants import ContentType
from content import Content


class ContentProcessor:
    def __init__(self, video_path: str, audio_path: str, combined_path: str):
        self.video_path = video_path
        self.audio_path = audio_path
        self.combined_path = combined_path

    def combine_audio_video(
        self, video_filename: str, audio_filename: str, output_filename: str
    ):
        """Combines audio and video files into a single file"""
        video_path = os.path.join(self.video_path, video_filename)
        audio_path = os.path.join(self.audio_path, audio_filename)
        output_path = os.path.join(self.combined_path, output_filename)

        input_video = ffmpeg.input(video_path)
        input_audio = ffmpeg.input(audio_path)

        ffmpeg.concat(input_video, input_audio, v=1, a=1).output(output_path).run()
        print(f"Combined video saved to: {output_path}")

    def split_content(
        self,
        chunk_duration: int,
        content: Content,
    ) -> list[Content]:
        """Splits a video or audio file into chunks of a specified duration"""

        filename = content.filepath.split("/")[-1]
        input_path = content.filepath

        if content.content_type == ContentType.VIDEO:
            output_path = self.video_path
        elif content.content_type == ContentType.AUDIO:
            output_path = self.audio_path
        elif content.content_type == ContentType.COMBINED:
            output_path = self.combined_path

        # Get the duration of the input file
        probe = ffmpeg.probe(input_path)
        duration = float(probe["format"]["duration"])

        # Check if the file is shorter than the chunk duration
        if duration < chunk_duration:
            raise ValueError(
                f"File duration is shorter than the chunk duration: {duration} < {chunk_duration}"
            )

        # Split the video into chunks
        num_chunks = int(duration // chunk_duration) + 1

        output = []
        for i in range(num_chunks):
            print(f"Splitting chunk {i+1} of {num_chunks}...")
            start_time = i * chunk_duration
            current_duration = min(chunk_duration, duration - start_time)
            if current_duration > 0:
                filename = filename.split(".")[0]
                output_file = os.path.join(output_path, f"{filename}_{i:03d}.mp4")

                # Create a copy of the input content and update the details (filepath, duration)
                content_chunk = content.copy()
                content_chunk.filepath = output_file
                content_chunk.duration = chunk_duration

                output.append(content_chunk)
                ffmpeg.input(input_path, ss=start_time, t=current_duration).output(
                    output_file
                ).run()

        return output
