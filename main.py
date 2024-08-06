from downloader import YouTubeDownloader
from pytubefix import Playlist


def main():
    url = input("Enter the YouTube video or playlist URL: ")

    if "playlist" in url.lower():
        playlist = Playlist(url)
        choice = input(
            "Download (v)ideo, (a)udio, (b)oth, or (c)ombined for all videos in the playlist? "
        ).lower()

        for video in playlist.videos:
            downloader = YouTubeDownloader(video.watch_url)
            downloader.handle_download(choice)

    else:
        downloader = YouTubeDownloader(url)
        choice = input("Download (v)ideo, (a)udio, (b)oth, or (c)ombined? ").lower()
        downloader.handle_download(choice)


if __name__ == "__main__":
    main()
