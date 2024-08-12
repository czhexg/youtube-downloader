# YouTube Video Downloader

## Overview

The YouTube Video Downloader is a Python-based tool that allows you to download videos and audio from YouTube. You can download individual videos, entire playlists, or both video and audio combined into a single file. The tool also supports processing the downloaded content, such as combining audio and video files.

## Features

- **Download Options**: Download video, audio, or both.
- **Playlist Support**: Download all videos in a playlist.
- **Combining Media**: Merge video and audio into a single file.
- **Multithreading**: Simultaneous downloading of video and audio for faster performance.

## Prerequisites

- Python 3.x
- Required Python packages:
  - `pytubefix`
  - `ffmpeg-python`
  
You can install the required packages using pip:

```bash
pip install pytubefix ffmpeg-python
```

**Note:** You must have `ffmpeg` installed on your system. If you don't have it, you can download it from the [official website](https://www.ffmpeg.org/download.html) and add it to your system's PATH.

## Usage

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/yourusername/youtube-downloader.git
   cd youtube-downloader
   ```

2. **Run the Script:**

   Execute the `main.py` script to start the downloader:

   ```bash
   python main.py
   ```

3. **Enter the URL:**

   - When prompted, enter the URL of the YouTube video or playlist you want to download.
   - For a single video, just paste the video URL.
   - For a playlist, paste the playlist URL.

4. **Choose Download Option:**

   - `v` - Download video only.
   - `a` - Download audio only.
   - `b` - Download both video and audio separately.
   - `c` - Download video and audio and combine them into a single file.

5. **Access Your Files:**

   - The downloaded files will be saved in the `youtube_vids` directory within your current working directory.
   - The directory contains separate folders for `video`, `audio`, and `combined` content.

## Example

```bash
Enter the YouTube video or playlist URL: https://www.youtube.com/watch?v=dQw4w9WgXcQ
Download (v)ideo, (a)udio, (b)oth, or (c)ombined? c
```

After the download completes, the combined file will be saved in the `youtube_vids/combined` directory.

## Notes

- The `split_content` feature is currently available in the code but is not used by default. This feature allows splitting large videos or audio files into smaller chunks. To enable and customize this feature, you would need to modify the code directly.