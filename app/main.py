import logging
from pathlib import Path

from app.scr import Services, exception_decorator, get_params
from app.settings import logger_setup

logger_setup()
logger = logging.getLogger(__name__)


@exception_decorator
def main(
    folder_with_images: Path,
    folder_for_images_without_exif: Path,
    is_clean_exif: bool,
    is_create_result_json: bool,
) -> None:
    """
    Main function to process image files in the specified directory.

    Parameters:
        folder_with_images (Path): Path to the folder containing the images.
        folder_for_images_without_exif (Path): Path to the folder
        where images without EXIF data will be saved.
        is_clean_exif (bool): Indicates whether to clean EXIF data from images.
        is_create_result_json (bool): Indicates whether to create a JSON file with EXIF data.

    Returns:
        None
    """
    images_path = Services.get_image_files_from_path(
        path=folder_with_images,
    )
    result_folder = Services.create_result_folder(
        name=folder_for_images_without_exif,
    )
    exif_data = Services.clean_exif(
        image_files=images_path,
        result_dock=is_create_result_json,
        result_folder=result_folder,
    )

    Services.create_json_file_with_exif(
        exif_data=exif_data,
        is_clean_exif=is_clean_exif,
        result_folder=result_folder,
    )


if __name__ == "__main__":
    input_params_for_script = get_params()

    main(
        folder_with_images=Path(
            input_params_for_script.image_folder_path,
        ).resolve(),
        folder_for_images_without_exif=Path(
            input_params_for_script.result_folder_path,
        ).resolve(),
        is_clean_exif=input_params_for_script.clean_exif,
        is_create_result_json=input_params_for_script.create_json,
    )
