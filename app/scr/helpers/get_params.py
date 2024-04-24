import argparse
from argparse import Namespace

# TODO: make like pass_changer


def get_params() -> Namespace:
    """
    Parse command line arguments to get parameters for processing images.

    Returns:
        Namespace: A namespace containing the parsed arguments.
            - image_folder_path (str): Path to images folder.
            - result_folder_path (str): Path to folder where save images without exif data.
            - create_json (bool): Create Json file with exif image data.
            - clean_exif (bool): Clean exif from images.
    """
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-ifp",
        "--image_folder_path",
        type=str,
        required=True,
        help="Path to images folder.",
    )
    parser.add_argument(
        "-rfp",
        "--result_folder_path",
        type=str,
        required=True,
        help="Path to folder where save images without exif data.",
    )
    parser.add_argument(
        "-cj",
        "--create_json",
        type=bool,
        default=True,
        required=False,
        help="Create Json file with exif image data.",
    )
    parser.add_argument(
        "-cle",
        "--clean_exif",
        type=bool,
        default=True,
        required=False,
        help="Clean exif from images.",
    )

    args = parser.parse_args()

    return args
