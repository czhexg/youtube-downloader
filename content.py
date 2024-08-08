from abc import ABC

from constants import ContentType


class Content(ABC):
    def __init__(
        self,
        title: str,
        duration: int,
        creator: str,
        filepath: str,
        content_type: ContentType = None,
        description: str = None,
        thumbnail: str = None,
    ):
        if self.__class__ is Content:
            raise TypeError(
                "Content is an abstract class and cannot be instantiated directly."
            )

        self.title = title
        self.duration = duration  # duration in seconds
        self.description = description
        self.creator = creator
        self.filepath = filepath
        self.thumbnail = thumbnail
        self.content_type = content_type

    def info(self):
        print(f"Title: {self.title}")
        print(f"Duration: {self.duration} seconds")
        print(f"Creator: {self.creator}")
        print(f"Description: {self.description}")
        print(f"Thumbnail URL: {self.thumbnail}")
        print(f"Filepath: {self.filepath}")
        print(f"Content Type: {self.content_type.value}")


class Video(Content):
    def __init__(
        self, title, duration, creator, filepath, description, thumbnail, resolution
    ):
        super().__init__(title, duration, creator, filepath, description, thumbnail)
        self.resolution = resolution
        self.content_type = ContentType.VIDEO

    def info(self):
        super().info()
        print(f"Resolution: {self.resolution}")


class Audio(Content):
    def __init__(
        self, title, duration, creator, filepath, description, thumbnail, bitrate
    ):
        super().__init__(title, duration, creator, filepath, description, thumbnail)
        self.bitrate = bitrate
        self.content_type = ContentType.AUDIO

    def info(self):
        super().info()
        print(f"Bitrate: {self.bitrate}")


class CombinedContent(Content):
    def __init__(
        self,
        title,
        duration,
        creator,
        filepath,
        description,
        thumbnail,
        resolution,
        bitrate,
    ):
        super().__init__(title, duration, creator, filepath, description, thumbnail)
        self.resolution = resolution
        self.bitrate = bitrate
        self.content_type = ContentType.COMBINED

    def info(self):
        super().info()
        print(f"Resolution: {self.resolution}")
