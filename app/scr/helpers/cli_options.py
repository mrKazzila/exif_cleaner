import argparse
from argparse import ArgumentParser, Namespace
from collections import namedtuple

__all__ = {"get_options"}

arg_param = namedtuple(
    "Params",
    "short_flag, flag, type, required, default, help",
)


def get_options() -> Namespace:
    """
    Parse command line arguments to get parameters for processing images.

    Returns:
        Namespace: A namespace containing the parsed arguments.
            - image_folder_path (str): Path to images folder.
            - result_folder_path (str): Path to folder where save images without exif data.
            - create_json (bool): Create Json file with exif image data.
            - clean_exif (bool): Clean exif from images.
    """
    _parser = argparse.ArgumentParser(
        description="Your program description here.",
    )

    parser = _add_options(parser=_parser)

    return parser.parse_args()


def _add_options(parser: ArgumentParser) -> ArgumentParser:
    _args = (
        arg_param(
            "-i",
            "--input-folder",
            type=str,
            required=True,
            default=None,
            help="Specify the path to the folder containing images.",
        ),
        arg_param(
            "-o",
            "--output-folder",
            type=str,
            required=True,
            default=None,
            help="Specify the path to the folder where images without EXIF data will be saved.",
        ),
        arg_param(
            "-j",
            "--create-json",
            type=bool,
            required=False,
            default=True,
            help="Flag to indicate whether to create a JSON file with EXIF image data.",
        ),
        arg_param(
            "-ce",
            "--clean-exif",
            type=bool,
            required=False,
            default=True,
            help="Flag to indicate whether to clean EXIF data from images.",
        ),
    )

    for arg in _args:
        parser.add_argument(
            arg.short_flag,
            arg.flag,
            type=arg.type,
            required=arg.required,
            default=arg.default,
            help=arg.help,
        )
    return parser
