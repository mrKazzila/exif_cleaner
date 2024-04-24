import logging
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path

from PIL import Image, ImageOps
from PIL.ExifTags import TAGS
from PIL.Image import Exif
from pillow_heif import register_heif_opener

from app.scr.helpers.types import ExifResultData

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

        Args:
            result_folder (Path): Folder for images without exif.
        """
        result = {"data": []}
        result_data = result["data"]

        with ProcessPoolExecutor() as executor:
            to_do = {
                executor.submit(
                    self._pop_metadata_from_image,
                    image_path,
                    result_folder / image_path.name,
                )
                for image_path in self.files
            }

            [
                result_data.append(future.result())
                for future in as_completed(to_do)
            ]

        return result if self.is_create_result_json else None

    def _pop_metadata_from_image(
        self,
        original_file_path: Path,
        new_file_path: Path,
    ):
        """
        Rewrite an image without its metadata.

        Args:
            original_file_path (Path): The path to the original image file.
            new_file_path (Path): The path where the new image will be saved.
        """
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
            exif_data = self._get_exif_data_from_image(
                image_object=image_object,
                image_name=original_file_path.name,
            )

        self._rewrite_image_without_exif(
            image_object=image_object,
            new_file_path=new_file_path,
        )

        image_object.close()

        if self.is_create_result_json:
            return exif_data

    def _get_exif_data_from_image(
        self,
        image_object: Image,
        image_name: Path.name,
    ):
        if exif_data := image_object.getexif():
            logger.debug("File: %s", image_name)
            exif_tags = self._print_exif_tags(exif_data=exif_data)

            return {
                "file_name": image_name,
                "exif_data": exif_tags,
            }

        logger.debug("Image %s contains no meta-information.", image_name)
        return {
            "file_name": image_name,
            "exif_data": None,
        }

    @staticmethod
    def _print_exif_tags(exif_data: Exif) -> dict[str, str]:
        """
        Print EXIF metadata tags and their values.

        Args:
            exif_data (PIL.Image.Exif): The EXIF metadata.

        Returns:
            dict
        """
        return {
            str(TAGS.get(tag, tag)): str(value)
            for tag, value in exif_data.items()
        }

    @staticmethod
    def _rewrite_image_without_exif(
        image_object: Image,
        new_file_path: Path.name,
    ):
        original = ImageOps.exif_transpose(image_object)
        stripped = Image.new(original.mode, original.size)

        data = list(original.getdata())
        stripped.putdata(data)

        stripped.save(new_file_path)
