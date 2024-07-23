import logging
from collections.abc import Sequence
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path
from time import perf_counter

from PIL import Image, ImageOps
from PIL.ExifTags import TAGS
from PIL.Image import Exif
from pillow_heif import register_heif_opener

from cleaner.src.helpers.types import ExifResultData, FileExifData

__all__ = ("ExifCleaner",)

logger = logging.getLogger(__name__)
register_heif_opener()


class ExifCleaner:
    __slots__ = ("files", "is_create_result_json")

    def __init__(self, *, files: list[Path], is_create_result_json):
        self.files = files
        self.is_create_result_json = is_create_result_json

    def clean_exif(self, *, result_folder: Path) -> ExifResultData | None:
        """
        Cleans the EXIF metadata from the provided list of image files.
        """
        start_time = perf_counter()

        result = {"data": []}
        result_data = result["data"]
        result_time = result["time"]

        with ProcessPoolExecutor() as executor:
            futures = {
                executor.submit(
                    self._process_image,
                    image_path,
                    result_folder / image_path.name,
                )
                for image_path in self.files
            }

            [
                result_data.append(future.result())
                for future in as_completed(futures)
            ]

        result_time["time"] = perf_counter() - start_time

        return result if self.is_create_result_json else None

    def _process_image(
        self,
        original_file_path: Path,
        new_file_path: Path,
    ) -> FileExifData | None:
        """Rewrite an image without its metadata."""
        try:
            image_object: Image.Image = Image.open(original_file_path)
        except OSError as error_:
            logger.error(
                "Error when reading image file %s: %s",
                original_file_path.name,
                error_,
            )
            raise error_

        exif_data = None

        if self.is_create_result_json:
            exif_data = self._get_exif_data(
                image_object=image_object,
                image_name=original_file_path.name,
            )

        self._rewrite_image(
            image_object=image_object,
            new_file_path=new_file_path,
        )

        image_object.close()

        return exif_data

    def _get_exif_data(
        self,
        *,
        image_object: Image.Image,
        image_name: str,
    ) -> FileExifData:
        """Retrieve and format EXIF metadata from an image."""
        try:
            if exif_data := image_object.getexif():
                logger.info("File: %s", image_name)
                return FileExifData(
                    file_name=image_name,
                    exif_tags=self._format_exif_tags(exif_data=exif_data),
                )

            logger.info("Image %s contains no meta-information", image_name)
            return FileExifData(
                file_name=image_name,
                exif_tags=None,
            )
        except OSError as error_:
            logger.error(
                "Error when retrieving exif data for a file %s: %s",
                image_name,
                error_,
            )
            return FileExifData(
                file_name=image_name,
                exif_tags=None,
            )

    @staticmethod
    def _format_exif_tags(*, exif_data: Exif) -> dict[str, str]:
        """Format EXIF metadata into a dictionary."""
        return {
            str(TAGS.get(tag, tag)): str(value)
            for tag, value in exif_data.items()
        }

    @staticmethod
    def _rewrite_image(
        *,
        image_object: Image.Image,
        new_file_path: Path,
    ) -> None:
        """Rewrite an image without its EXIF metadata."""
        try:
            if original := ImageOps.exif_transpose(image_object):
                _data = original.getdata()
                data = list(_data)

                stripped = Image.new(original.mode, original.size)
                stripped.putdata(data)
                stripped.save(new_file_path)

        except OSError as error_:
            logger.error("Error when overwriting an image file: %s", error_)
