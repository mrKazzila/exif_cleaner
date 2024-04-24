import json
import logging
from functools import lru_cache
from pathlib import Path
from typing import TypeAlias

from PIL import Image, ImageOps
from pillow_heif import register_heif_opener

from app.settings import FILES_FORMAT, ROOT_DIR

logger = logging.getLogger(__name__)
register_heif_opener()
ExifResultData: TypeAlias = dict[str, list[dict[str, str]]]


class FileManager:
    @classmethod
    def get_image_files_from_path(cls, path: Path) -> list[Path]:
        """
        Retrieves a list of image files from a given directory path.

        Args:
            path (Path): The directory path to search for image files.

        Returns:
            list[Path]: A list of Path objects representing the image files found.
        """
        images_path = [
            file
            for file in path.rglob("*")
            if file.is_file() and file.suffix.lower() in FILES_FORMAT
        ]
        logger.info("Get %s images from dir: %s", len(images_path), path.name)

        return images_path

    @classmethod
    @lru_cache
    def create_result_folder(cls, folder_name: Path) -> Path:
        """
        Create a result folder if it doesn't exist.

        Parameters:
            folder_name (Path): Path to the folder.

        Returns:
            Path: Path to the created folder.
        """
        if folder_name.exists() and folder_name.is_dir():
            logger.warning("%s already exist!", folder_name)
            return folder_name

        folder_name.mkdir(parents=True)
        logger.info("%s: created!", folder_name)

        return folder_name

    @classmethod
    def create_json_file_with_exif(cls, data: dict, file_path: Path) -> None:
        """
        Create a JSON file containing EXIF data.

        Parameters:
            data (dict): Dictionary containing the EXIF data to be stored in the JSON file.
            file_path (Path): Path to the JSON file.

        Returns:
            None
        """
        with open(file_path, "w", encoding="utf-8") as jf:
            json.dump(data, jf, indent=3, ensure_ascii=False)

        logger.info("Result file %s was created!", file_path)

    @classmethod
    def create_path_for_result_json(cls, is_clean_exif, result_folder: Path):
        return (
            ROOT_DIR / "result.json"
            if not is_clean_exif
            else result_folder / "result.json"
        )

    @classmethod
    def _rewrite_image_without_metadata(
        cls,
        original_file_path: Path,
        new_file_path: Path,
    ) -> None:
        """
        Rewrite an image without its metadata.

        Args:
            original_file_path (Path): The path to the original image file.
            new_file_path (Path): The path where the new image will be saved.
        """
        try:
            original = Image.open(original_file_path)
        except OSError as e:
            logger.error(
                "ERROR: Problem reading image file %s.",
                original_file_path.name,
            )
            raise e

        original = ImageOps.exif_transpose(original)
        stripped = Image.new(original.mode, original.size)

        data = list(original.getdata())
        stripped.putdata(data)
        stripped.save(new_file_path)
