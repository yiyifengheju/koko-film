"""
=========================================================================
@File Name: sub_marker_4.py
@Time: 2025/6/11 00:05
@Program IDE: PyCharm
@Create by Author: 一一风和橘
@Motto: "The trick, William Potter, is not minding that it hurts."
@Description:
-
-
=========================================================================
"""

from PIL import Image, ImageDraw, ImageFont

from koko_film.common.base import ArchImages
from koko_film.common.config import config
from koko_film.koko_marker.base import generate_border


class PARAM:
    border_width = 250
    border = [0, border_width, 0, 0]
    color = (255, 255, 255, 255)
    loc = (0, 0)
    font_size = 40
    font = ImageFont.FreeTypeFont(font=config.FONTS.LATO, size=font_size)
    txt_color = (0, 0, 0)
    logo_size = (int(border_width / 4 * 5.9), int(border_width / 4))


def sub_marker_4(
    marker_exif: ArchImages,
    image: Image,
    w: int,
    h: int,
):
    img = generate_border(
        w,
        h,
        PARAM.border,
        color=PARAM.color,
    )

    img.paste(image, PARAM.loc)
    draw = ImageDraw.Draw(img)

    text_2 = f"{marker_exif.FOCAL_LENGTH}  f/{marker_exif.F_NUMBER}  {marker_exif.EXPOSURE_TIME}  ISO{marker_exif.ISO}"
    bbox = draw.textbbox((0, 0), text_2, PARAM.font)
    text_width = bbox[2] - bbox[0]
    txt_loc_2 = (
        int(w * 0.5 - text_width / 2),
        int(h + PARAM.border_width / 5 * 3),
    )
    draw.text(xy=txt_loc_2, text=text_2, fill=PARAM.txt_color, font=PARAM.font)

    logo_loc = (
        int(w * 0.5 - PARAM.logo_size[0] / 2),
        int(h + PARAM.border_width / 3.5),
    )
    logo = Image.open(config.LOGO.FUJIFILM).convert("RGBA").resize(PARAM.logo_size)
    solid_layer = img.crop(
        (
            logo_loc[0],
            logo_loc[1],
            logo_loc[0] + PARAM.logo_size[0],
            logo_loc[1] + PARAM.logo_size[1],
        ),
    )
    logo = Image.alpha_composite(solid_layer, logo)
    img.paste(logo, logo_loc)
    return img
