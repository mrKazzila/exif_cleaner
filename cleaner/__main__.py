from pathlib import Path

from cleaner.settings import logger_setup
from cleaner.src import process_images, exception_decorator, get_options


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
    logger_setup()
    main()
