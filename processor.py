import ffmpeg

import os


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
