"""
=========================================================================
@File Name: _marker_2.py
@Time: 2025/6/10 00:46
@Program IDE: PyCharm
@Create by Author: 一一风和橘
@Motto: "The trick, William Potter, is not minding that it hurts."
@Description:
-
-
=========================================================================
"""

from PIL import Image, ImageDraw, ImageFilter, ImageFont

try:
    from koko_marker.base_operator import MarkerEXIF, generate_border
    from koko_marker.config import FONTS_CFG, LOGO_CFG
except ImportError:
    from koko_film.koko_marker.base_operator import MarkerEXIF, generate_border
    from koko_film.koko_marker.config import FONTS_CFG, LOGO_CFG


class PARAM:
    border_width = 150
    border = [
        int(border_width / 3),
        int(border_width * 5 / 3),
        int(border_width),
        int(border_width),
    ]
    logo_size = (int(border_width / 2 * 5.9), int(border_width / 2))
    loc = (150, 50)
    color = (255, 255, 255, 255)
    font_size = 48
    font = ImageFont.FreeTypeFont(font=FONTS_CFG.FONT_LATO, size=font_size)
    THEME = "dark"
    LOGO = LOGO_CFG.LOGO_FUJIFILM_PURE if THEME == "dark" else LOGO_CFG.LOGO_FUJIFILM
    txt_color = (255, 255, 255) if THEME == "dark" else (0, 0, 0)


def _sub_marker_2(marker_exif: MarkerEXIF):
    img = generate_border(
        marker_exif.width,
        marker_exif.height,
        PARAM.border,
        color=PARAM.color,
    )
    tmp = marker_exif.image.resize(
        (
            marker_exif.width + PARAM.border_width * 2,
            marker_exif.height + PARAM.border_width * 2,
        ),
    )
    blurred_img = tmp.filter(ImageFilter.GaussianBlur(radius=50))
    img.paste(blurred_img, (0, 0))
    img.paste(marker_exif.image, (PARAM.loc[0], PARAM.loc[1]))
    draw = ImageDraw.Draw(img)

    text_2 = (
        f"{marker_exif.focal_length}mm  f/{marker_exif.f_number:.1f}  {marker_exif.exposure_time}  ISO{marker_exif.iso}"
    )
    bbox = draw.textbbox((0, 0), text_2, PARAM.font)
    text_width = bbox[2] - bbox[0]
    txt_loc_2 = (
        int(marker_exif.width * 0.5 - text_width / 2 + PARAM.border_width),
        int(marker_exif.height + PARAM.border_width * 1.3),
    )
    draw.text(
        xy=txt_loc_2,
        text=text_2,
        fill=PARAM.txt_color,
        font=PARAM.font,
    )

    logo = Image.open(PARAM.LOGO).convert("RGBA").resize(PARAM.logo_size)
    logo_loc = (
        int(marker_exif.width * 0.5 - PARAM.logo_size[0] / 2 + PARAM.border_width),
        int(marker_exif.height + PARAM.border_width / 1.5),
    )
    solid_layer = blurred_img.crop(
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
