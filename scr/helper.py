import json
import logging
from pathlib import Path
from typing import Any, TypeAlias

from PIL import Image, ImageOps
from PIL.ExifTags import TAGS
from PIL.Image import Exif
from pillow_heif import register_heif_opener
from settings import FILES_FORMAT

logger = logging.getLogger(__name__)
register_heif_opener()
ExifResultData: TypeAlias = dict[str, list[dict[str, str]]]


def get_image_files_from_path(path: Path) -> list[Path]:
    """
    Retrieves a list of image files from a given directory path.

    Args:
        path (Path): The directory path to search for image files.

    Returns:
        list[Path]: A list of Path objects representing the image files found.
    """
    images_path = [file for file in path.rglob('*') if file.is_file() and file.suffix.lower() in FILES_FORMAT]
    logger.info('Get %(images_path_len)s images from dir: %(path_name)s',
                {'images_path_len': len(images_path), 'path_name': path.name})

    return images_path


def check_exif_is_exist(images_path: list[Path]) -> ExifResultData:
    """
    Checks if exits are present in the provided list of image files.

    Args:
        images_path (list[Path]): A list of Path objects representing image files.
    """
    result = {'data': []}

    for index, image_path in enumerate(images_path):
        exit_info = _get_exif_from_image(image_path=image_path)
        result['data'].append(exit_info)

    return result


def create_result_folder(folder_name: Path) -> Path:
    """
    Create a result folder if it doesn't exist.

    Parameters:
        folder_name (Path): Path to the folder.

    Returns:
        Path: Path to the created folder.
    """
    if folder_name.exists() and folder_name.is_dir():
        logger.warning('%s already exist!', folder_name)
        return folder_name

    folder_name.mkdir(parents=True)
    logger.info('%s: created!', folder_name)

    return folder_name


def clean_exif(images_path: list[Path], result_folder: Path) -> None:
    """
    Cleans the EXIF metadata from the provided list of image files.

    Args:
        images_path (list[Path]): A list of Path objects representing image files.
        result_folder (Path): Folder for images without exif.
    """
    for image_path in images_path:
        _rewrite_image_without_metadata(
            original_file_path=image_path,
            new_file_path=result_folder / image_path.name,
        )


def create_json_file_with_exif(data: dict, file_path: Path) -> None:
    """
    Create a JSON file containing EXIF data.

    Parameters:
        data (dict): Dictionary containing the EXIF data to be stored in the JSON file.
        file_path (Path): Path to the JSON file.

    Returns:
        None
    """
    with open(file_path, 'w', encoding='utf-8') as jf:
        json.dump(data, jf, indent=3, ensure_ascii=False)

    logger.info('Result file %s was created!', file_path)


def _rewrite_image_without_metadata(original_file_path: Path, new_file_path: Path) -> None:
    """
    Rewrite an image without its metadata.

    Args:
        original_file_path (Path): The path to the original image file.
        new_file_path (Path): The path where the new image will be saved.
    """
    try:
        original = Image.open(original_file_path)
    except IOError as e:
        logger.error('ERROR: Problem reading image file %s.', original_file_path.name)
        raise e

    original = ImageOps.exif_transpose(original)
    stripped = Image.new(original.mode, original.size)

    data = list(original.getdata())
    stripped.putdata(data)
    stripped.save(new_file_path)


def _get_exif_from_image(image_path: Path) -> dict[str, Any]:
    """
    Extract EXIF metadata from an image and log it.

    Args:
        image_path (Path): The path to the image file.

    Returns:
        None
    """
    image_object = Image.open(image_path)

    if exif_data := image_object.getexif():
        logger.debug('File: %s', image_path.name)
        exif_tags = _print_exif_tags(exif_data=exif_data)
        image_object.close()

        return {
            'file_name': image_path.name,
            'exif_data': exif_tags,
        }

    logger.info('Image %s contains no meta-information.', image_path.name)
    image_object.close()

    return {
        'file_name': image_path.name,
        'exif_data': None,
    }


def _print_exif_tags(exif_data: Exif) -> dict[str, str]:
    """
    Print EXIF metadata tags and their values.

    Args:
        exif_data (PIL.Image.Exif): The EXIF metadata.

    Returns:
        dict
    """
    result = {}

    for tag, value in exif_data.items():
        tag_name = TAGS.get(tag, tag)

        result[str(tag_name)] = str(value)
        logger.debug('%(tag_name)s: %(value)s', {'tag_name': tag_name, 'value': value})

    return result
