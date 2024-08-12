# YouTube Video Downloader: Technical Documentation

## Overview

This project is a Python-based YouTube video downloader that allows users to download videos, audio, or both, either separately or combined, from YouTube. The program supports downloading individual videos or entire playlists. It uses the `pytubefix` library for downloading media content and `ffmpeg` for processing media files.

The codebase is structured to be modular and extensible, with different responsibilities divided into separate classes and files. This documentation will guide you through the project structure, class responsibilities, and how to extend the functionality.

## Project Structure

The project is organized into the following files:

- **constants.py**: Defines constants and enumerations used throughout the project.
- **content.py**: Contains the abstract `Content` class and its concrete subclasses (`Video`, `Audio`, and `CombinedContent`), which represent different types of media content.
- **downloader.py**: Implements the `YouTubeDownloader` class responsible for downloading content from YouTube.
- **processor.py**: Contains the `ContentProcessor` class, which handles processing tasks such as combining video and audio, and splitting content into chunks.
- **main.py**: The entry point of the application, handling user input and orchestrating the downloading process.

## File Details

### constants.py

- **`ContentType`**: An enumeration that defines the types of content that can be handled by the application: `VIDEO`, `AUDIO`, and `COMBINED`.

### content.py

This file contains the base `Content` class and its specialized subclasses:

- **`Content` (abstract base class)**: 
  - Attributes: 
    - `title`: The title of the content.
    - `duration`: The duration of the content in seconds.
    - `creator`: The creator (author) of the content.
    - `filename`: The filename under which the content is saved.
    - `filepath`: The path where the content is stored.
    - `description`: A brief description of the content.
    - `thumbnail`: The URL to the content's thumbnail.
    - `content_type`: The type of content (as defined in `ContentType`).
  - Methods:
    - `info()`: Prints detailed information about the content.
    - `copy()`: An abstract method that subclasses must implement to return a copy of the content object (returns a new object with the copied attributes of the original object).

- **`Video` (subclass of `Content`)**: Represents video content.
  - Additional Attribute: `resolution` (e.g., 1080p, 720p).
  - Overrides: `info()` to include resolution and `copy()` to return a copy of a `Video` object.

- **`Audio` (subclass of `Content`)**: Represents audio content.
  - Additional Attribute: `bitrate` (e.g., 128kbps).
  - Overrides: `info()` to include bitrate and `copy()` to return a copy of an `Audio` object.

- **`CombinedContent` (subclass of `Content`)**: Represents combined audio and video content.
  - Additional Attributes: `resolution`, `bitrate`.
  - Overrides: `info()` to include resolution and bitrate, and `copy()` to return a copy of a `CombinedContent` object.

### downloader.py

This file contains the `YouTubeDownloader` class, responsible for downloading YouTube content:

- **`YouTubeDownloader`**:
  - Attributes:
    - `url`: The URL of the YouTube video or playlist.
    - `yt`: A `YouTube` object from `pytubefix`.
    - `title`: The sanitized title of the content.
    - `retries`: The number of retries for downloading.
    - `base_path`: The base directory where content will be saved.
    - `video_path`, `audio_path`, `combined_path`: Directories for saving video, audio, and combined content, respectively.
    - `processor`: An instance of `ContentProcessor` for processing content.
  - Methods:
    - `_create_directories()`: Creates directories for saving content.
    - `_download_with_retries()`: Downloads a stream with retries in case of failure.
    - `download_video()`: Downloads the highest resolution video stream with the `avc1` codec.
    - `download_audio()`: Downloads the highest quality audio stream.
    - `download_both()`: Downloads both video and audio using multithreading.
    - `handle_download()`: Handles user choices for downloading and, optionally, processing content (e.g., combining video and audio, splitting content).

### processor.py

This file contains the `ContentProcessor` class, which handles processing tasks:

- **`ContentProcessor`**:
  - Attributes:
    - `video_path`: Path to save video content.
    - `audio_path`: Path to save audio content.
    - `combined_path`: Path to save combined content.
  - Methods:
    - `combine_audio_video()`: Combines a video file with an audio file into a single file.
    - `split_content()`: Splits a video or audio file into chunks of a specified duration (currently not in use).

### main.py

- **Main Functionality**:
  - Prompts the user for a YouTube video or playlist URL.
  - Determines if the URL is for a single video or a playlist.
  - Prompts the user to choose between downloading video, audio, both, or combined.
  - Creates a `YouTubeDownloader` instance and initiates the download based on user input.
  - For playlists, iterates over each video in the playlist and applies the selected download operation.

## Extending the Functionality

### Adding New Content Types
To add new content types:
1. Define a new type in `ContentType` in `constants.py`.
2. Create a new subclass of `Content` in `content.py` with the necessary attributes and methods.
3. Update the `YouTubeDownloader` and `ContentProcessor` classes if the new content type requires special handling during download or processing.

### Using the Split Content Method
The `split_content` method in `ContentProcessor` is not currently utilized. If you wish to split downloaded content:
1. Call the `handle_download()` method, setting the `to_split` parameter to true and specifying the `chunk_duration` method:  
 `downloader.handle_download(choice, to_split=True, chunk_duration=chunk_duration)`  

### Handling Errors and Exceptions
To improve error handling:
- Expand the retry logic in `_download_with_retries()` to cover more exceptions or different retry strategies.
- Add error handling in `combine_audio_video()` and `split_content()` methods to manage ffmpeg-related errors.

## Conclusion

This documentation provides an overview of the codebase and guidance on extending its functionality. With this structure, developers can quickly understand how to add new features, improve existing ones, and maintain the codebase effectively. The modular design allows for easy updates and modifications, making the project scalable for future enhancements.