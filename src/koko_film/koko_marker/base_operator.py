"""
=========================================================================
@File Name: base_operator.py
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
    image: Image.Image
    filename: str
    aim_size: int
    path_dst: str
    artist: str
    width: int
    height: int
    focal_length: float
    f_number: float
    exposure_time: str
    iso: int
    cam_make: str
    cam_model: str
    lens_make: str
    lens_model: str
    shot_time: datetime
    logo: str
    logo_pure: str


@validate_call
def validate_exif(data: dict) -> MarkerEXIF:
    return MarkerEXIF(**data)
