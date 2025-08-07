"""
=========================================================================
@File Name: sub_marker_6.py
@Time: 2025/6/9 23:56
@Program IDE: PyCharm
@Create by Author: 一一风和橘
@Motto: "The trick, William Potter, is not minding that it hurts."
@Description:
- 柯南片尾水印
-
=========================================================================
"""

from PIL import Image, ImageDraw, ImageFont

from koko_film.common.base import DictImages
from koko_film.common.config import config


class PARAM:
    border_width = 150
    font_size = 72
    font = ImageFont.FreeTypeFont(font=config.FONTS.NOTO_JP, size=font_size)
    THEME = "dark"
    txt_color = (255, 255, 255) if THEME == "dark" else (0, 0, 0)
    text = "原   作\n青 山 剛 昌\n小学館「週刊少年サンデー」連載中"
    stroke_width = 3
    stroke_color = "black"


def sub_marker_conan(
    marker_exif: DictImages,
    image: Image,
    w: int,
    h: int,
):
    draw = ImageDraw.Draw(image)
    bbox = draw.textbbox((0, 0), PARAM.text, PARAM.font)
    text_width = bbox[2] - bbox[0]
    txt_loc_2 = (
        int(w * 0.5 - text_width / 2),
        int(h - PARAM.border_width / 0.4),
    )
    draw.text(
        xy=txt_loc_2,
        text=PARAM.text,
        fill=PARAM.txt_color,
        font=PARAM.font,
        stroke_width=PARAM.stroke_width,
        stroke_fill=PARAM.stroke_color,
        align="center",
    )
    return image
