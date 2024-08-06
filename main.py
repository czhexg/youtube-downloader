from downloader import YouTubeDownloader

import threading


def main():
    url = input("Enter the YouTube video URL: ")
    downloader = YouTubeDownloader(url)

    choice = input("Download (v)ideo, (a)udio, or (b)oth? ").lower()

    if choice == "v":
        downloader.download_video()
    elif choice == "a":
        downloader.download_audio()
    elif choice == "b":
        downloader.download_both()

        # Combine audio and video
        downloader.combine_audio_video(
            f"{downloader.title}_video.mp4",
            f"{downloader.title}_audio.mp3",
            f"{downloader.title}_combined.mp4",
        )
    else:
        print("Invalid choice. Exiting.")


if __name__ == "__main__":
    main()
