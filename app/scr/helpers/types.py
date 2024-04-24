from typing import TypeAlias

__all__ = ("ExifResultData",)

ExifResultData: TypeAlias = dict[str, list[dict[str, str]]]
