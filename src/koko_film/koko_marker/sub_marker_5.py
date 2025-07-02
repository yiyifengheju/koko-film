"""
=========================================================================
@File Name: sub_marker_5.py
@Time: 2025/6/11 00:05
@Program IDE: PyCharm
@Create by Author: 一一风和橘
@Motto: "The trick, William Potter, is not minding that it hurts."
@Description:
-
-
=========================================================================
"""

from typing import Literal

from PIL import Image, ImageDraw, ImageFont

from koko_film.common.base import ArchImages
from koko_film.common.config import config


class PARAM:
    border_width = 120
    logo_size = (int(border_width / 2 * 5.9), int(border_width / 2))
    loc = (150, 50)
    color = (255, 255, 255, 255)
    font_size = 48
    font = ImageFont.FreeTypeFont(font=config.FONTS.LATO, size=font_size)
    THEME = "dark"
    LOGO = {
        "dark": config.LOGO.FUJIFILM_PURE,
        "light": config.LOGO.FUJIFILM,
    }
    txt_color = {
        "dark": (255, 255, 255),
        "light": (0, 0, 0),
    }


def sub_marker_5(
    marker_exif: ArchImages,
    image: Image,
    w: int,
    h: int,
    theme: Literal["dark", "light"] = "dark",
):
    draw = ImageDraw.Draw(image)
    text_2 = f"{marker_exif.FOCAL_LENGTH}  f/{marker_exif.F_NUMBER}  {marker_exif.EXPOSURE_TIME}  ISO{marker_exif.ISO}"
    bbox = draw.textbbox((0, 0), text_2, PARAM.font)
    text_width = bbox[2] - bbox[0]
    txt_loc_2 = (
        int(w * 0.5 - text_width / 2),
        int(h - PARAM.border_width / 1.1),
    )
    draw.text(
        xy=txt_loc_2,
        text=text_2,
        fill=PARAM.txt_color[theme],
        font=PARAM.font,
    )

    logo = Image.open(PARAM.LOGO[theme]).convert("RGBA").resize(PARAM.logo_size)
    logo_loc = (
        int(w * 0.5 - PARAM.logo_size[0] / 2),
        int(h - PARAM.border_width * 1.6),
    )
    solid_layer = image.crop(
        (
            logo_loc[0],
            logo_loc[1],
            logo_loc[0] + PARAM.logo_size[0],
            logo_loc[1] + PARAM.logo_size[1],
        ),
    )
    logo = Image.alpha_composite(solid_layer, logo)
    image.paste(logo, logo_loc)
    return image
