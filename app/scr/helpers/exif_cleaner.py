import logging
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path

from PIL import Image, ImageOps
from PIL.ExifTags import TAGS
from PIL.Image import Exif
from pillow_heif import register_heif_opener

from app.scr.helpers.types import ExifResultData

__all__ = ("ExifCleaner",)

logger = logging.getLogger(__name__)
register_heif_opener()


class ExifCleaner:
    __slots__ = ("files", "is_create_result_json")

    def __init__(self, files: list[Path], is_create_result_json):
        self.files = files
        self.is_create_result_json = is_create_result_json

    def clean_exif(self, result_folder: Path) -> ExifResultData | None:
        """
        Cleans the EXIF metadata from the provided list of image files.
        """
        result = {"data": []}
        result_data = result["data"]

        with ProcessPoolExecutor() as executor:
            futures = {
                executor.submit(
                    self._process_image,
                    image_path,
                    result_folder / image_path.name,
                )
                for image_path in self.files
            }

            for future in as_completed(futures):
                result_data.append(future.result())

        return result if self.is_create_result_json else None

    def _process_image(
        self,
        original_file_path: Path,
        new_file_path: Path,
    ):
        """Rewrite an image without its metadata."""
        try:
            image_object = Image.open(original_file_path)
        except OSError as error:
            logger.error(
                "ERROR: Problem reading image file %s.",
                original_file_path.name,
            )
            raise error

        exif_data = None

        if self.is_create_result_json:
            exif_data = self._get_exif_data(
                image_object,
                original_file_path.name,
            )

        self._rewrite_image(image_object, new_file_path)

        image_object.close()

        return exif_data

    def _get_exif_data(
        self,
        image_object: type[Image],
        image_name: str,
    ) -> dict[str, str]:
        """Retrieve and format EXIF metadata from an image."""
        result = {"file_name": image_name}
        exif_data = image_object.getexif()

        if exif_data:
            logger.debug("File: %s", image_name)
            result["exif_data"] = self._format_exif_tags(exif_data=exif_data)
            return result

        logger.debug("Image %s contains no meta-information.", image_name)
        return {"file_name": image_name, "exif_data": None}

    @staticmethod
    def _format_exif_tags(exif_data: Exif) -> dict[str, str]:
        """Format EXIF metadata into a dictionary."""
        return {
            str(TAGS.get(tag, tag)): str(value)
            for tag, value in exif_data.items()
        }

    @staticmethod
    def _rewrite_image(image_object: type[Image], new_file_path: Path) -> None:
        """Rewrite an image without its EXIF metadata."""
        original = ImageOps.exif_transpose(image_object)
        stripped = Image.new(original.mode, original.size)

        data = list(original.getdata())
        stripped.putdata(data)

        stripped.save(new_file_path)
