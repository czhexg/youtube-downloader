from downloader import YouTubeDownloader

import threading


def main():
    url = input("Enter the YouTube video URL: ")
    downloader = YouTubeDownloader(url)

    choice = input("Download (v)ideo, (a)udio, (b)oth, or (c)ombined? ").lower()

    if choice == "v":
        downloader.download_video()
    elif choice == "a":
        downloader.download_audio()
    elif choice == "b":
        downloader.download_both()
    elif choice == "c":
        downloader.download_both()

        # Combine audio and video
        video_filename = f"{downloader.yt.title}_video.mp4"
        audio_filename = f"{downloader.yt.title}_audio.mp3"
        output_filename = f"{downloader.yt.title}_combined.mp4"
        downloader.combine_audio_video(video_filename, audio_filename, output_filename)
    else:
        print("Invalid choice. Exiting.")


if __name__ == "__main__":
    main()
