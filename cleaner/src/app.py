from pathlib import Path

from cleaner.src.services import Services

__all__ = ("process_images",)


def process_images(
    *,
    image_folder: Path,
    result_folder: Path,
    clean_exif: bool,
    create_json: bool,
) -> None:
    """
    Process image files in the specified directory.

    Parameters:
        image_folder (Path): Path to the folder containing the images.
        result_folder (Path): Path to the folder where images without EXIF data will be saved.
        clean_exif (bool): Indicates whether to clean EXIF data from images.
        create_json (bool): Indicates whether to create a JSON file with EXIF data.

    Returns:
        None
    """
    images_path = Services.get_image_files(path=image_folder)
    result_folder = Services.create_result_folder(name=result_folder)

    exif_data = Services.clean_exif(
        image_files=images_path,
        create_json=create_json,
        result_folder=result_folder,
    )

    Services.create_json_file_with_exif(
        exif_data=exif_data,
        is_clean_exif=clean_exif,
        result_folder=result_folder,
    )
