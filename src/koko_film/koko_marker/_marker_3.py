"""
=========================================================================
@File Name: _marker_3.py
@Time: 2025/6/11 00:04
@Program IDE: PyCharm
@Create by Author: 一一风和橘
@Motto: "The trick, William Potter, is not minding that it hurts."
@Description:
-
-
=========================================================================
"""

from PIL import Image, ImageFilter

try:
    from koko_marker.base_operator import MarkerEXIF, generate_border
except ImportError:
    from koko_film.koko_marker.base_operator import MarkerEXIF, generate_border


class PARAM:
    border_width = 150
    border = [
        int(border_width / 3 * 2),
        int(border_width * 5 / 3),
        int(border_width),
        int(border_width),
    ]
    logo_size = (int(border_width / 2 * 5.9), int(border_width / 2))
    loc = (150, 100)
    color = (255, 255, 255, 255)


def _sub_marker_3(marker_exif: MarkerEXIF):
    img = generate_border(
        marker_exif.width,
        marker_exif.height,
        PARAM.border,
        color=PARAM.color,
    )
    shadow = Image.new(
        "RGBA",
        (
            marker_exif.width + int(PARAM.border_width / 3),
            marker_exif.height + int(PARAM.border_width / 3),
        ),
        (150, 150, 150, 255),
    )
    img.paste(
        shadow,
        (
            PARAM.loc[0] - int(PARAM.border_width / 6),
            PARAM.loc[1] - int(PARAM.border_width / 6),
        ),
    )
    img = img.filter(ImageFilter.GaussianBlur(50))

    img.paste(marker_exif.image, (PARAM.loc[0], PARAM.loc[1]))

    logo_size = (int(PARAM.border_width / 2 * 5.9), int(PARAM.border_width / 2))
    logo_loc = (
        int(marker_exif.width * 0.5 - logo_size[0] / 2 + PARAM.border_width),
        int(marker_exif.height + PARAM.border_width / 0.85),
    )

    logo = Image.open(marker_exif.logo).convert("RGBA").resize(logo_size)
    solid_layer = img.crop(
        (
            logo_loc[0],
            logo_loc[1],
            logo_loc[0] + logo_size[0],
            logo_loc[1] + logo_size[1],
        ),
    )
    logo = Image.alpha_composite(solid_layer, logo)
    img.paste(logo, logo_loc)

    return img
