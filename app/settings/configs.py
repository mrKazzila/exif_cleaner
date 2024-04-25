from pathlib import Path

__all__ = ("FILES_FORMAT", "ROOT_DIR")

FILES_FORMAT = (".jpg", ".jpeg", ".png", ".heic")

ROOT_DIR = Path(__file__).resolve().parent
