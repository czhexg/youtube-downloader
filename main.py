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
        # Create threads
        video_thread = threading.Thread(target=downloader.download_video())
        audio_thread = threading.Thread(target=downloader.download_audio())

        # Start threads
        video_thread.start()
        audio_thread.start()

        # Wait for both threads to complete
        video_thread.join()
        audio_thread.join()
    else:
        print("Invalid choice. Exiting.")


if __name__ == "__main__":
    main()
