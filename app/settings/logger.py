import logging
import logging.config as logging_config
from functools import lru_cache
from pathlib import Path
from sys import exit

import yaml

__all__ = ("logger_setup",)
logger = logging.getLogger(__name__)


@lru_cache
def logger_setup():
    logging_config_file = Path(Path(__file__).parent / "logger.yaml").resolve()

    try:
        with open(logging_config_file) as config_file:
            config = yaml.safe_load(config_file.read())
        logging_config.dictConfig(config)

    except FileNotFoundError as error_:
        logger.error("Error %s:", error_)
        exit(1)
