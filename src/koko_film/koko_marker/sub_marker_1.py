"""
=========================================================================
@File Name: sub_marker_1.py
@Time: 2025/6/10 00:23
@Program IDE: PyCharm
@Create by Author: 一一风和橘
@Motto: "The trick, William Potter, is not minding that it hurts."
@Description:
-
-
=========================================================================
"""

from PIL import Image, ImageDraw, ImageFont

from koko_film.common.base import DictImages
from koko_film.common.config import config
from koko_film.koko_marker.base import generate_border


class PARAM:
    border_width = 150
    border = [0, border_width, 0, 0]
    loc = (0, 0)
    layer_color = (255, 255, 255, 255)
    txt_color = (0, 0, 0)
    font_size_1 = 80
    font_size_2 = 48
    font_size_3 = 32
    font_1 = ImageFont.FreeTypeFont(font=config.FONTS.LATO, size=font_size_1)
    font_2 = ImageFont.FreeTypeFont(font=config.FONTS.LATO, size=font_size_2)
    font_3 = ImageFont.FreeTypeFont(font=config.FONTS.LATO, size=font_size_3)


def sub_marker_1(
    marker_exif: DictImages,
    image: Image,
    w: int,
    h: int,
):
    img = generate_border(
        w,
        h,
        PARAM.border,
        color=PARAM.layer_color,
    )
    img.paste(image, PARAM.loc)
    draw = ImageDraw.Draw(img)

    txt_loc_1 = (
        int(PARAM.border_width * 2 / 3),
        h + int(PARAM.border_width / 6),
    )
    text_1 = marker_exif.CAM_MODEL
    draw.text(xy=txt_loc_1, text=text_1, fill=PARAM.txt_color, font=PARAM.font_1)

    # 计算下后面的宽度
    text_2 = (
        f"{marker_exif.FOCAL_LENGTH}  "
        f"f/{marker_exif.F_NUMBER}  "
        f"{marker_exif.EXPOSURE_TIME}  "
        f"ISO{marker_exif.ISO}"
    )
    text_3 = f"{marker_exif.LENS_MAKE}  {marker_exif.LENS_MODEL}"

    bbox_2 = draw.textbbox((0, 0), text_2, PARAM.font_2)
    text_width_2 = bbox_2[2] - bbox_2[0]
    bbox_3 = draw.textbbox((0, 0), text_3, PARAM.font_3)
    text_width_3 = bbox_3[2] - bbox_3[0]
    text_max_width = max(text_width_2, text_width_3)

    txt_loc_2 = (
        int(w - text_max_width - PARAM.border_width / 3),
        int(h + PARAM.border_width / 7.5),
    )
    draw.text(xy=txt_loc_2, text=text_2, fill=PARAM.txt_color, font=PARAM.font_2)

    txt_loc_3 = (
        int(w - text_max_width - PARAM.border_width / 3),
        h + int(PARAM.border_width / 7 * 4),
    )
    draw.text(xy=txt_loc_3, text=text_3, fill=PARAM.txt_color, font=PARAM.font_3)

    line_loc = [
        (
            int(w - text_max_width - PARAM.border_width / 2),
            int(h + PARAM.border_width / 5),
        ),
        (
            int(w - text_max_width - PARAM.border_width / 2),
            int(h + PARAM.border_width * 4 / 5),
        ),
    ]
    draw.line(line_loc, width=3, fill=PARAM.txt_color)

    logo_size = (
        int(PARAM.border_width / 5 * 2 * 5.9),
        int(PARAM.border_width / 5 * 2),
    )
    logo_loc = (
        int(w - text_max_width - PARAM.border_width * 2 / 3 - logo_size[0]),
        int(h + PARAM.border_width / 3.5),
    )
    logo = Image.open(config.LOGO.FUJIFILM).convert("RGBA").resize(logo_size)
    solid_layer = Image.new("RGBA", logo_size, PARAM.layer_color)
    logo = Image.alpha_composite(solid_layer, logo)
    img.paste(logo, logo_loc)
    return img
