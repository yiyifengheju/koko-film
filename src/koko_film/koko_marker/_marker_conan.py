"""
=========================================================================
@File Name: _marker_conan.py
@Time: 2025/6/9 23:56
@Program IDE: PyCharm
@Create by Author: 一一风和橘
@Motto: "The trick, William Potter, is not minding that it hurts."
@Description:
-
-
=========================================================================
"""

from PIL import ImageDraw, ImageFont

try:
    from koko_marker.base_operator import MarkerEXIF
    from koko_marker.config import FONTS_CFG
except ImportError:
    from koko_film.koko_marker.base_operator import MarkerEXIF
    from koko_film.koko_marker.config import FONTS_CFG


class PARAM:
    border_width = 150
    font_size = 72
    font = ImageFont.FreeTypeFont(font=FONTS_CFG.FONT_NOTO_JP, size=font_size)
    THEME = "dark"
    txt_color = (255, 255, 255) if THEME == "dark" else (0, 0, 0)
    text = "原   作\n青 山 剛 昌\n小学館「週刊少年サンデー」連載中"
    stroke_width = 3
    stroke_color = "black"


def _sub_marker_conan(marker_exif: MarkerEXIF):
    draw = ImageDraw.Draw(marker_exif.image)
    bbox = draw.textbbox((0, 0), PARAM.text, PARAM.font)
    text_width = bbox[2] - bbox[0]
    txt_loc_2 = (
        int(marker_exif.width * 0.5 - text_width / 2),
        int(marker_exif.height - PARAM.border_width / 0.4),
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
    return marker_exif.image
