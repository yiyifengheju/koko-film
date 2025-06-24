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

try:
    from koko_marker.base_operator import generate_border
    from koko_marker.config import FONTS_CFG
except ImportError:
    from koko_film.koko_marker.base_operator import generate_border
    from koko_film.koko_marker.config import FONTS_CFG


class PARAM:
    border_width = 250
    border = [0, border_width, 0, 0]
    color = (255, 255, 255, 255)
    loc = (0, 0)
    font_size = 40
    font = ImageFont.FreeTypeFont(font=FONTS_CFG.FONT_LATO, size=font_size)
    txt_color = (0, 0, 0)
    logo_size = (int(border_width / 4 * 5.9), int(border_width / 4))


def sub_marker_4(marker_exif):
    img = generate_border(
        marker_exif.width,
        marker_exif.height,
        PARAM.border,
        color=PARAM.color,
    )

    img.paste(marker_exif.image, PARAM.loc)
    draw = ImageDraw.Draw(img)

    text_2 = (
        f"{marker_exif.FOCAL_LENGTH}mm  f/{marker_exif.F_NUMBER:.1f}  {marker_exif.EXPOSURE_TIME}  ISO{marker_exif.ISO}"
    )
    bbox = draw.textbbox((0, 0), text_2, PARAM.font)
    text_width = bbox[2] - bbox[0]
    txt_loc_2 = (
        int(marker_exif.width * 0.5 - text_width / 2),
        int(marker_exif.height + PARAM.border_width / 5 * 3),
    )
    draw.text(xy=txt_loc_2, text=text_2, fill=PARAM.txt_color, font=PARAM.font)

    logo_loc = (
        int(marker_exif.width * 0.5 - PARAM.logo_size[0] / 2),
        int(marker_exif.height + PARAM.border_width / 3.5),
    )
    logo = Image.open(marker_exif.logo).convert("RGBA").resize(PARAM.logo_size)
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
