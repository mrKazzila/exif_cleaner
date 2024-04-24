import logging
from pathlib import Path
from typing import TypeAlias

from app.scr.helpers import ExifCleaner, FileManager

logger = logging.getLogger(__name__)

ExifResultData: TypeAlias = dict[str, list[dict[str, str]]]


class Services:
    @classmethod
    def get_image_files_from_path(cls, *, path: Path) -> list[Path]:
        return FileManager.get_image_files_from_path(path=path)

    @classmethod
    def create_result_folder(cls, *, name: Path) -> Path:
        return FileManager.create_result_folder(folder_name=name)

    @classmethod
    def clean_exif(
        cls,
        *,
        image_files: list[Path],
        result_dock: bool,
        result_folder: Path,
    ):
        cleaner = ExifCleaner(
            files=image_files,
            is_create_result_json=result_dock,
        )
        return cleaner.clean_exif(result_folder=result_folder)

    @classmethod
    def create_json_file_with_exif(
        cls,
        *,
        exif_data,
        is_clean_exif: bool,
        result_folder: Path,
    ) -> None:
        if exif_data:
            file_path = FileManager.create_path_for_result_json(
                is_clean_exif=is_clean_exif,
                result_folder=result_folder,
            )
            FileManager.create_json_file_with_exif(
                data=exif_data,
                file_path=file_path,
            )
