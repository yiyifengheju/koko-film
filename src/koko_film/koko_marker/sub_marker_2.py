"""
=========================================================================
@File Name: sub_marker_2.py
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

from koko_film.common.base import DictImages
from koko_film.common.config import config
from koko_film.koko_marker.base import generate_border


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
    font = ImageFont.FreeTypeFont(font=config.FONTS.LATO, size=font_size)
    THEME = "dark"
    LOGO = config.LOGO.FUJIFILM_PURE if THEME == "dark" else config.LOGO.FUJIFILM
    txt_color = (255, 255, 255) if THEME == "dark" else (0, 0, 0)


def sub_marker_2(
    marker_exif: DictImages,
    image: Image,
    w: int,
    h: int,
) -> Image:
    img = generate_border(
        w,
        h,
        PARAM.border,
        color=PARAM.color,
    )
    tmp = image.resize(
        (
            w + PARAM.border_width * 2,
            h + PARAM.border_width * 2,
        ),
    )
    blurred_img = tmp.filter(ImageFilter.GaussianBlur(radius=50))
    img.paste(blurred_img, (0, 0))
    img.paste(image, (PARAM.loc[0], PARAM.loc[1]))
    draw = ImageDraw.Draw(img)

    text_2 = f"{marker_exif.FOCAL_LENGTH}  f/{marker_exif.F_NUMBER}  {marker_exif.EXPOSURE_TIME}  ISO{marker_exif.ISO}"
    bbox = draw.textbbox((0, 0), text_2, PARAM.font)
    text_width = bbox[2] - bbox[0]
    txt_loc_2 = (
        int(w * 0.5 - text_width / 2 + PARAM.border_width),
        int(h + PARAM.border_width * 1.3),
    )
    draw.text(
        xy=txt_loc_2,
        text=text_2,
        fill=PARAM.txt_color,
        font=PARAM.font,
    )

    logo = Image.open(PARAM.LOGO).convert("RGBA").resize(PARAM.logo_size)
    logo_loc = (
        int(w * 0.5 - PARAM.logo_size[0] / 2 + PARAM.border_width),
        int(h + PARAM.border_width / 1.5),
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
