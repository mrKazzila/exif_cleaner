import json
import logging
from functools import lru_cache
from pathlib import Path

from app.scr.helpers.types import ExifResultData
from app.settings import FILES_FORMAT, ROOT_DIR

logger = logging.getLogger(__name__)


class FileManager:
    @classmethod
    def get_image_files(cls, path: Path) -> list[Path]:
        """
        Retrieve a list of image files from the specified directory.

        Args:
            path (Path): The directory path to search for image files.

        Returns:
            List[Path]: A list of Path objects representing the image files found.
        """
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
        """
        Create a result folder if it doesn't exist.

        Args:
            folder_path (Path): The path to the folder to be created.

        Returns:
            Path: The path to the created folder.
        """
        if folder_path.exists() and folder_path.is_dir():
            logger.warning("Folder '%s' already exists!", folder_path)
            return folder_path

        folder_path.mkdir(parents=True)
        logger.info("Folder '%s' created!", folder_path)
        return folder_path

    @classmethod
    def save_json_file(cls, data: ExifResultData, file_path: Path) -> None:
        """
        Save data to a JSON file.

        Args:
            data (Dict): The data to be saved to the JSON file.
            file_path (Path): The path to the JSON file.

        Returns:
            None
        """
        with open(file_path, "w", encoding="utf-8") as json_file:
            json.dump(data, json_file, indent=3, ensure_ascii=False)

        logger.info("Result file '%s' created!", file_path)

    @classmethod
    def get_result_json_path(
        cls,
        is_clean_exif: bool,
        result_folder: Path,
    ) -> Path:
        """
        Get the path for the result JSON file.

        Args:
            is_clean_exif (bool): Indicates whether EXIF data is cleaned.
            result_folder (Path): The path to the result folder.

        Returns:
            Path: The path to the result JSON file.
        """
        return (
            ROOT_DIR / "result.json"
            if not is_clean_exif
            else result_folder / "result.json"
        )
