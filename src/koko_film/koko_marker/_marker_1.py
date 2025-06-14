"""
=========================================================================
@File Name: _marker_1.py
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

try:
    from koko_marker.base_operator import MarkerEXIF, generate_border
    from koko_marker.config import FONTS_CFG
except ImportError:
    from koko_film.koko_marker.base_operator import MarkerEXIF, generate_border
    from koko_film.koko_marker.config import FONTS_CFG


class PARAM:
    border_width = 150
    border = [0, border_width, 0, 0]
    loc = (0, 0)
    layer_color = (255, 255, 255, 255)
    txt_color = (0, 0, 0)
    font_size_1 = 80
    font_size_2 = 48
    font_size_3 = 32
    font_1 = ImageFont.FreeTypeFont(font=FONTS_CFG.FONT_LATO, size=font_size_1)
    font_2 = ImageFont.FreeTypeFont(font=FONTS_CFG.FONT_LATO, size=font_size_2)
    font_3 = ImageFont.FreeTypeFont(font=FONTS_CFG.FONT_LATO, size=font_size_3)


def _sub_marker_1(marker_exif: MarkerEXIF):
    img = generate_border(
        marker_exif.width,
        marker_exif.height,
        PARAM.border,
        color=PARAM.layer_color,
    )
    img.paste(marker_exif.image, PARAM.loc)
    draw = ImageDraw.Draw(img)

    txt_loc_1 = (
        int(PARAM.border_width * 2 / 3),
        marker_exif.height + int(PARAM.border_width / 6),
    )
    text_1 = marker_exif.cam_model
    draw.text(xy=txt_loc_1, text=text_1, fill=PARAM.txt_color, font=PARAM.font_1)

    # 计算下后面的宽度
    text_2 = (
        f"{marker_exif.focal_length}mm  "
        f"f/{marker_exif.f_number:.1f}  "
        f"{marker_exif.exposure_time}  "
        f"ISO{marker_exif.iso}"
    )
    text_3 = f"{marker_exif.lens_make}  {marker_exif.lens_model}"

    bbox_2 = draw.textbbox((0, 0), text_2, PARAM.font_2)
    text_width_2 = bbox_2[2] - bbox_2[0]
    bbox_3 = draw.textbbox((0, 0), text_3, PARAM.font_3)
    text_width_3 = bbox_3[2] - bbox_3[0]
    text_max_width = max(text_width_2, text_width_3)

    txt_loc_2 = (
        int(marker_exif.width - text_max_width - PARAM.border_width / 3),
        int(marker_exif.height + PARAM.border_width / 7.5),
    )
    draw.text(xy=txt_loc_2, text=text_2, fill=PARAM.txt_color, font=PARAM.font_2)

    txt_loc_3 = (
        int(marker_exif.width - text_max_width - PARAM.border_width / 3),
        marker_exif.height + int(PARAM.border_width / 7 * 4),
    )
    draw.text(xy=txt_loc_3, text=text_3, fill=PARAM.txt_color, font=PARAM.font_3)

    line_loc = [
        (
            int(marker_exif.width - text_max_width - PARAM.border_width / 2),
            int(marker_exif.height + PARAM.border_width / 5),
        ),
        (
            int(marker_exif.width - text_max_width - PARAM.border_width / 2),
            int(marker_exif.height + PARAM.border_width * 4 / 5),
        ),
    ]
    draw.line(line_loc, width=3, fill=PARAM.txt_color)

    logo_size = (
        int(PARAM.border_width / 5 * 2 * 5.9),
        int(PARAM.border_width / 5 * 2),
    )
    logo_loc = (
        int(marker_exif.width - text_max_width - PARAM.border_width * 2 / 3 - logo_size[0]),
        int(marker_exif.height + PARAM.border_width / 3.5),
    )
    logo = Image.open(marker_exif.logo).convert("RGBA").resize(logo_size)
    solid_layer = Image.new("RGBA", logo_size, PARAM.layer_color)
    logo = Image.alpha_composite(solid_layer, logo)
    img.paste(logo, logo_loc)
    return img
