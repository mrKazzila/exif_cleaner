import json
import logging
from functools import lru_cache
from pathlib import Path

from cleaner.src.helpers.types import ExifResultData
from cleaner.settings import FILES_FORMAT, ROOT_DIR

__all__ = ("FileManager",)

logger = logging.getLogger(__name__)


class FileManager:
    @classmethod
    def get_image_files(cls, path: Path) -> list[Path]:
        """Retrieve a list of image files from the specified directory."""
        images_path = [
            file
            for file in path.rglob("*")
            if file.is_file() and file.suffix.lower() in FILES_FORMAT
        ]
        logger.info(
            "Retrieved %s image(s) from directory: %s",
            len(images_path),
            path.name,
        )
        return images_path

    @classmethod
    @lru_cache
    def create_result_folder(cls, folder_path: Path) -> Path:
        """Create a result folder if it doesn't exist."""
        if folder_path.exists() and folder_path.is_dir():
            logger.warning("Folder '%s' already exists!", folder_path)
            return folder_path

        folder_path.mkdir(parents=True)
        logger.info("Folder '%s' created!", folder_path)
        return folder_path

    @classmethod
    def save_json_file(cls, data: ExifResultData, file_path: Path) -> None:
        """Save data to a JSON file."""
        with open(file_path, "w", encoding="utf-8") as json_file:
            json.dump(data, json_file, indent=3, ensure_ascii=False)

        logger.info("Result file '%s' created!", file_path)

    @classmethod
    def get_result_json_path(
        cls,
        is_clean_exif: bool,
        result_folder: Path,
    ) -> Path:
        """Get the path for the result JSON file."""
        return (
            ROOT_DIR / "result.json"
            if not is_clean_exif
            else result_folder / "result.json"
        )
