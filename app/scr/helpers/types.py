from typing import TypeAlias, TypedDict

__all__ = ("ExifResultData", "FileExifData")


class FileExifData(TypedDict):
    file_name: str
    exif_tags: dict[str, str] | None


ExifResultData: TypeAlias = dict[str, list[FileExifData | None]]
