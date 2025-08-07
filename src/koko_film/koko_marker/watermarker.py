"""
=========================================================================
@File Name: watermarker.py
@Time: 2024/5/13 上午3:13
@Program IDE：PyCharm
@Create by Author: 一一风和橘
@Motto: "The trick, William Potter, is not minding that it hurts."
@Description:
-
-
=========================================================================
"""

from concurrent.futures import ThreadPoolExecutor
from functools import partial
from pathlib import Path

import pandas as pd
import tqdm
from PIL import Image

from koko_film.common.base import PathBase
from koko_film.common.config import config
from koko_film.koko_marker.sub_marker_1 import sub_marker_1
from koko_film.koko_marker.sub_marker_2 import sub_marker_2
from koko_film.koko_marker.sub_marker_3 import sub_marker_3
from koko_film.koko_marker.sub_marker_4 import sub_marker_4
from koko_film.koko_marker.sub_marker_5 import sub_marker_5
from koko_film.koko_marker.sub_marker_6 import sub_marker_conan
from koko_film.raf_tools.raf_archive import get_exif


class KokoWaterMark:
    def __init__(
        self,
        path_root: str,
        select_style: list[str] | None = None,
        aim_width: int = 2560,
        aim_size: int = 500,
    ):
        self.aim_width = aim_width
        self.aim_size = aim_size
        self.path_marker = PathBase(path_root)
        self.select_style = (
            select_style
            if select_style is not None
            else [
                "MARK_0",
                "MARK_1",
                "MARK_2",
                "MARK_3",
                "MARK_4",
                "MARK_5",
                "MARK_CONAN",
            ]
        )
        self.webp_size = {}

    def marker(self, file):
        marker_exif = get_exif(file)
        self.webp_size[file.name] = {"INIT_SIZE": marker_exif.INIT_SIZE}

        image = Image.open(file).convert("RGBA")
        w, h, image = self._resize_img(image)

        images = {
            "MARK_0": partial(sub_marker_1, marker_exif, image.copy(), w, h),
            "MARK_1": partial(sub_marker_2, marker_exif, image.copy(), w, h),
            "MARK_2": partial(sub_marker_3, marker_exif, image.copy(), w, h),
            "MARK_3": partial(sub_marker_4, marker_exif, image.copy(), w, h),
            "MARK_4": partial(sub_marker_5, marker_exif, image.copy(), w, h, theme="dark"),
            "MARK_5": partial(sub_marker_5, marker_exif, image.copy(), w, h, theme="light"),
            "MARK_CONAN": partial(sub_marker_conan, marker_exif, image.copy(), w, h),
        }
        for style in self.select_style:
            img = images[style]()
            quality = config.APP.QUALITY_INIT
            file_path = Path(self.path_marker.webp, f"{marker_exif.FILENAME}_{style}.webp")
            img.save(file_path, "WEBP", quality=quality)
            webp_size = Path(file_path).stat().st_size

            while webp_size > self.aim_size * 1024:
                quality -= 2
                img.save(file_path, "WEBP", quality=quality)
                webp_size = Path(file_path).stat().st_size
            self.webp_size[file.name][style] = webp_size

    def webp_report(self):
        cols = ["FILE", "INIT_MEM"] + [f"{style}_MEM" for style in self.select_style] + ["RATE"]
        return pd.DataFrame(
            self.webp_size,
            columns=cols,
        )

    def run(self):
        files = list(Path(self.path_marker.jpg).glob("*.[jp][pn]g"))
        for file in files:
            self.marker(file)

        # with ThreadPoolExecutor(max_workers=6) as executor:
        #     _ = [executor.submit(self.marker, f) for f in files]

    def _resize_img(self, img):
        if img.size[0] > img.size[1]:
            h = int(self.aim_width * img.size[1] / img.size[0])
            w = self.aim_width
        else:
            w = int(self.aim_width * img.size[0] / img.size[1])
            h = self.aim_width
        img = img.resize((w, h))
        return w, h, img


def example():
    my_watermarker = KokoWaterMark(
        path_root=r"H:\200_RAF\20250607",
        aim_size=1024,
    )
    my_watermarker.run()


if __name__ == "__main__":
    example()
