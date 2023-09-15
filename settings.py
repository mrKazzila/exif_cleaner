import logging
from pathlib import Path

IS_DEBUG = False
FILES_FORMAT = ('.jpg', '.jpeg', '.png')

ROOT_DIR = Path(__file__).resolve().parent

logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s %(module)s [%(name)s:%(lineno)s] %(message)s',
    datefmt='%d/%b/%Y %H:%M:%S',
)
