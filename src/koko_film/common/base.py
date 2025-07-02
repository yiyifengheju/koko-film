"""
=========================================================================
@File Name: base.py
@Time: 2025/6/28 13:43
@Program IDE: PyCharm
@Create by Author: 一一风和橘
@Motto: "The trick, William Potter, is not minding that it hurts."
@Description:
-
-
=========================================================================
"""

from dataclasses import dataclass
from pathlib import Path


@dataclass
class ArchSummary:
    DATE: str = ""
    CAM_MODEL: str | list[str] = ""
    LENS_MODEL: str | list[str] = ""
    PROVINCE: str = ""
    CITY: str = ""
    DISTRICT: str = ""
    SCENIC_SPOT: str | list[str] = ""
    PERSON: str = ""
    TAGS: str | list[str] = ""
    ARCHIVED: str | list[str] = ""
    RANK: str = ""


@dataclass
class ArchSync:
    NAS_SYNC: bool = False
    NAS_PATH: str = ""
    SYNC_DATE: str = ""


@dataclass
class ArchImages:
    FILENAME: str = ""
    SHOT_TIME: str = ""
    INIT_SIZE: int = ""
    ARTIST: str = ""
    WIDTH: int = ""
    HEIGHT: int = ""
    FOCAL_LENGTH: str = ""
    F_NUMBER: str = ""
    EXPOSURE_TIME: str = ""
    ISO: str = ""
    CAM_MAKE: str = ""
    CAM_MODEL: str = ""
    LENS_MAKE: str = ""
    LENS_MODEL: str = ""
    PATH_RAF: str = ""
    PATH_JPG: list = ""
    PATH_WEBP: list = ""


@dataclass
class Arch:
    SUMMARY: ArchSummary
    SYNC: ArchSync
    IMAGES: dict[str, "ArchImages"]

class PathArchiveCls:
    def __init__(self, root: str):
        self.root = Path(root)
        self.toml = Path(root, "Archive.toml")
        self.raf = Path(root, "RAF")
        self.jpg = Path(root, "JPG")
        self.webp = Path(root, "WEBP")
        for item in [self.raf, self.jpg, self.webp]:
            item.mkdir(parents=True, exist_ok=True)
        if not self.toml.exists():
            self.toml.touch(exist_ok=True)
