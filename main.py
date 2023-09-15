import logging
from pathlib import Path

from scr.decorator import exception_decorator
from scr.get_params import get_params
from scr.helper import (
    check_exif_is_exist,
    clean_exif,
    create_json_file_with_exif,
    create_result_folder,
    get_image_files_from_path,
)
from settings import IS_DEBUG, ROOT_DIR

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
        folder_for_images_without_exif (Path): Path to the folder where images without EXIF data will be saved.
        is_clean_exif (bool): Indicates whether to clean EXIF data from images.
        is_create_result_json (bool): Indicates whether to create a JSON file with EXIF data.

    Returns:
        None
    """
    images_path = get_image_files_from_path(path=folder_with_images)
    data = check_exif_is_exist(images_path=images_path)

    if is_clean_exif:
        result_folder = create_result_folder(folder_name=folder_for_images_without_exif)

        clean_exif(
            images_path=images_path,
            result_folder=folder_for_images_without_exif,
        )

        # check after clean
        if IS_DEBUG:
            result_folder_images_path = get_image_files_from_path(result_folder)
            check_exif_is_exist(images_path=result_folder_images_path)

    if is_create_result_json:
        file_path = ROOT_DIR / 'result.json' if not is_clean_exif else folder_for_images_without_exif / 'result.json'
        create_json_file_with_exif(
            data=data,
            file_path=file_path,
        )


if __name__ == '__main__':
    input_params_for_script = get_params()

    main(
        folder_with_images=Path(input_params_for_script.image_folder_path).resolve(),
        folder_for_images_without_exif=Path(input_params_for_script.result_folder_path).resolve(),
        is_clean_exif=input_params_for_script.clean_exif,
        is_create_result_json=input_params_for_script.create_json,
    )
