from downloader import YouTubeDownloader


def main():
    url = input("Enter the YouTube video URL: ")
    downloader = YouTubeDownloader(url)

    choice = input("Download (v)ideo, (a)udio, or (b)oth? ").lower()

    if choice == "v":
        downloader.download_video()
    elif choice == "a":
        downloader.download_audio()
    elif choice == "b":
        downloader.download_video()
        downloader.download_audio()
    else:
        print("Invalid choice. Exiting.")


if __name__ == "__main__":
    main()
