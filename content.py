from abc import ABC, abstractmethod

from constants import ContentType


class Content(ABC):
    def __init__(
        self,
        title: str,
        duration: int,
        creator: str,
        filename: str,
        filepath: str,
        description: str = None,
        thumbnail: str = None,
        content_type: ContentType = None,
    ):
        self.title = title
        self.duration = duration
        self.creator = creator
        self.filename = filename
        self.filepath = filepath
        self.description = description
        self.thumbnail = thumbnail
        self.content_type = content_type

    def info(self):
        print(f"Title: {self.title}")
        print(f"Duration: {self.duration} seconds")
        print(f"Creator: {self.creator}")
        print(f"Filename: {self.filename}")
        print(f"Filepath: {self.filepath}")
        print(f"Description: {self.description}")
        print(f"Thumbnail: {self.thumbnail}")
        print(f"Content Type: {self.content_type.value}")

    @abstractmethod
    def copy(self):
        pass


class Video(Content):
    def __init__(
        self,
        title,
        duration,
        creator,
        filename,
        filepath,
        description,
        thumbnail,
        resolution,
    ):
        super().__init__(
            title, duration, creator, filename, filepath, description, thumbnail
        )
        self.resolution = resolution
        self.content_type = ContentType.VIDEO

    def info(self):
        super().info()
        print(f"Resolution: {self.resolution}")

    def copy(self):
        return Video(
            title=self.title,
            duration=self.duration,
            creator=self.creator,
            filename=self.filename,
            filepath=self.filepath,
            description=self.description,
            thumbnail=self.thumbnail,
            resolution=self.resolution,
        )


class Audio(Content):
    def __init__(
        self,
        title,
        duration,
        creator,
        filename,
        filepath,
        description,
        thumbnail,
        bitrate,
    ):
        super().__init__(
            title, duration, creator, filename, filepath, description, thumbnail
        )
        self.bitrate = bitrate
        self.content_type = ContentType.AUDIO

    def info(self):
        super().info()
        print(f"Bitrate: {self.bitrate}")

    def copy(self):
        return Audio(
            title=self.title,
            duration=self.duration,
            creator=self.creator,
            filename=self.filename,
            filepath=self.filepath,
            description=self.description,
            thumbnail=self.thumbnail,
            bitrate=self.bitrate,
        )


class CombinedContent(Content):
    def __init__(
        self,
        title,
        duration,
        creator,
        filename,
        filepath,
        description,
        thumbnail,
        resolution,
        bitrate,
    ):
        super().__init__(
            title, duration, creator, filename, filepath, description, thumbnail
        )
        self.resolution = resolution
        self.bitrate = bitrate
        self.content_type = ContentType.COMBINED

    def info(self):
        super().info()
        print(f"Resolution: {self.resolution}")

    def copy(self):
        return CombinedContent(
            title=self.title,
            duration=self.duration,
            creator=self.creator,
            filename=self.filename,
            filepath=self.filepath,
            description=self.description,
            thumbnail=self.thumbnail,
            resolution=self.resolution,
            bitrate=self.bitrate,
        )
