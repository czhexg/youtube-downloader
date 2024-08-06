from downloader import YouTubeDownloader

import threading


def main():
    url = input("Enter the YouTube video URL: ")
    downloader = YouTubeDownloader(url)

    choice = input("Download (v)ideo, (a)udio, (b)oth, or (c)ombined? ").lower()

    downloader.handle_download(choice)


if __name__ == "__main__":
    main()
