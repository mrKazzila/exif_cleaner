import logging
from pathlib import Path

from app.scr import Services, exception_decorator, get_options
from app.settings import logger_setup

logger_setup()
logger = logging.getLogger(__name__)


def process_images(
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


@exception_decorator
def main() -> None:
    """
    Main function to process image files with specified parameters.
    """
    input_params = get_options()

    image_folder = Path(input_params.input_folder).resolve()
    result_folder = Path(input_params.output_folder).resolve()

    process_images(
        image_folder=image_folder,
        result_folder=result_folder,
        clean_exif=input_params.clean_exif,
        create_json=input_params.create_json,
    )


if __name__ == "__main__":
    main()
