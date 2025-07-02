"""
=========================================================================
@File Name: test.py
@Time: 2025/6/27 22:09
@Program IDE: PyCharm
@Create by Author: 一一风和橘
@Motto: "The trick, William Potter, is not minding that it hurts."
@Description:
- 
- 
=========================================================================
"""
import toml
from PIL import Image
from datetime import datetime
from dataclasses import dataclass, field
from typing import Any

@dataclass
class KokoImages:
    FILENAME: str
    SHOT_TIME: str
    INIT_SIZE:int
    ARTIST: str
    WIDTH: int
    HEIGHT: int
    FOCAL_LENGTH: str
    F_NUMBER: str
    EXPOSURE_TIME: str
    ISO: str
    CAM_MAKE: str
    CAM_MODEL: str
    LENS_MAKE: str
    LENS_MODEL: str
    PATH_RAF: str
    PATH_JPG: list
    PATH_WEBP: list

    def to_toml(self, path_toml: str) -> None:
        pass

if __name__ == '__main__':
    a = MarkerEXIF(
        IMAGE=None,
    )