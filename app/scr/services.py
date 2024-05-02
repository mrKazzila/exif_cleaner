import logging
from pathlib import Path

from app.scr.helpers import ExifCleaner, ExifResultData, FileManager

__all__ = ("Services",)

logger = logging.getLogger(__name__)


class Services:
    @classmethod
    def get_image_files(cls, *, path: Path) -> list[Path]:
        """Retrieve image files from the specified path."""
        return FileManager.get_image_files(path=path)

    @classmethod
    def create_result_folder(cls, *, name: Path) -> Path:
        """Create a result folder with the specified name."""
        return FileManager.create_result_folder(folder_path=name)

    @classmethod
    def clean_exif(
        cls,
        *,
        image_files: list[Path],
        create_json: bool,
        result_folder: Path,
    ) -> ExifResultData | None:
        """Clean EXIF data from image files."""
        cleaner = ExifCleaner(
            files=image_files,
            is_create_result_json=create_json,
        )
        return cleaner.clean_exif(result_folder=result_folder)

    @classmethod
    def create_json_file_with_exif(
        cls,
        *,
        exif_data: ExifResultData | None,
        is_clean_exif: bool,
        result_folder: Path,
    ) -> None:
        """Create a JSON file with EXIF data."""
        if exif_data:
            file_path = FileManager.get_result_json_path(
                is_clean_exif=is_clean_exif,
                result_folder=result_folder,
            )
            FileManager.save_json_file(data=exif_data, file_path=file_path)
