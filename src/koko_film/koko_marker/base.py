"""
=========================================================================
@File Name: base.py
@Time: 2025/6/10 00:38
@Program IDE: PyCharm
@Create by Author: 一一风和橘
@Motto: "The trick, William Potter, is not minding that it hurts."
@Description:
-
-
=========================================================================
"""

from dataclasses import dataclass
from datetime import datetime

from PIL import Image
from pydantic import validate_call


def generate_border(
    width,
    height,
    border: list | None = None,
    color: tuple | None = None,
):
    if border is None:
        border = [150, 150, 150, 150]
    if color is None:
        color = (255, 255, 255, 255)
    width = width + border[2] + border[3]
    height = height + border[1] + border[0]
    return Image.new("RGBA", (width, height), color)


@dataclass
class MarkerEXIF:
    IMAGE: Image.Image
    FILENAME: str
    AIM_SIZE: int
    PATH_DST: str
    ARTIST: str
    WIDTH: int
    HEIGHT: int
    FOCAL_LENGTH: float
    F_NUMBER: float
    EXPOSURE_TIME: str
    ISO: int
    CAM_MAKE: str
    CAM_MODEL: str
    LENS_MAKE: str
    LENS_MODEL: str
    SHOT_TIME: datetime
    LOGO: str
    LOGO_PURE: str


@validate_call
def validate_exif(data: dict) -> MarkerEXIF:
    return MarkerEXIF(**data)
