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

import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from pathlib import Path
from typing import Literal

import exifread
import pandas as pd
import tqdm
from PIL import Image

try:
    from koko_marker.sub_marker_1 import sub_marker_1
    from koko_marker.sub_marker_2 import sub_marker_2
    from koko_marker.sub_marker_3 import sub_marker_3
    from koko_marker.sub_marker_4 import sub_marker_4
    from koko_marker.sub_marker_5 import sub_marker_5
    from koko_marker.sub_marker_conan import sub_marker_conan
    from koko_marker.base_operator import MarkerEXIF, validate_exif
    from koko_marker.config import APP_CFG, LOGO_CFG
except ImportError:
    from koko_film.koko_marker.sub_marker_1 import sub_marker_1
    from koko_film.koko_marker.sub_marker_2 import sub_marker_2
    from koko_film.koko_marker.sub_marker_3 import sub_marker_3
    from koko_film.koko_marker.sub_marker_4 import sub_marker_4
    from koko_film.koko_marker.sub_marker_5 import sub_marker_5
    from koko_film.koko_marker.sub_marker_conan import sub_marker_conan
    from koko_film.koko_marker.base_operator import MarkerEXIF, validate_exif
    from koko_film.koko_marker.config import APP_CFG, LOGO_CFG


class Marker:
    def __init__(
        self,
        marker_exif: MarkerEXIF,
    ):
        self.marker_exif = marker_exif

    def run(self, style, aim_size):
        match style:
            case "MARK_0":
                img = sub_marker_1(self.marker_exif)
            case "MARK_1":
                img = sub_marker_2(self.marker_exif)
            case "MARK_2":
                img = sub_marker_3(self.marker_exif)
            case "MARK_3":
                img = sub_marker_4(self.marker_exif)
            case "MARK_4":
                img = sub_marker_5(self.marker_exif, theme="dark")
            case "MARK_5":
                img = sub_marker_5(self.marker_exif, theme="light")
            case "MARK_CONAN":
                img = sub_marker_conan(self.marker_exif)
            case _:
                img = None

        quality = APP_CFG.QUALITY_INIT
        file_path = Path(
            self.marker_exif.path_dst, f"{self.marker_exif.filename}_{style}.webp"
        )
        img.save(file_path, "WEBP", quality=quality)
        webp_size = Path(file_path).stat().st_size

        while webp_size > aim_size * 1024:
            quality -= 2
            img.save(file_path, "WEBP", quality=quality)
            webp_size = Path(file_path).stat().st_size
        return img


class KokoWaterMark:
    def __init__(
        self,
        path_src: str,
        path_dst: str,
        aim_width: int = 2560,
        aim_size: int = 500,
        watermark_style: Literal[
            "MARK_0",
            "MARK_1",
            "MARK_2",
            "MARK_3",
            "MARK_4",
            "MARK_5",
            "MARK_CONAN",
        ] = "MARK_0",
        camera_make: Literal["FujiFilm", "SONY"] = "FujiFilm",
        init_info: dict | None = None,
    ):
        self.path_src = path_src
        self.path_dst = path_dst
        self.aim_width = aim_width
        self.aim_size = aim_size
        self.watermark_style = watermark_style
        self.camera_make = camera_make
        if init_info is None:
            self.init_info = {"Image Artist": "Artmallo"}

    def _check(self):
        if not Path(self.path_dst).exists():
            Path(self.path_dst).mkdir(parents=True)
        return True

    def _core(self, file):
        try:
            exif = self.get_exif(file)
            marker = Marker(exif)
            marker.run(self.watermark_style, self.aim_size)
        except KeyError:
            return

    def _get_report(self):
        size_list = []
        files = os.listdir(self.path_src)
        for file in files:
            filename = file.split(".")[0]
            old_size = Path(f"{self.path_src}/{file}").stat().st_size
            new_size = (
                Path(f"{self.path_dst}/{filename}_{self.watermark_style}.webp")
                .stat()
                .st_size
            )
            size_list.append([filename, old_size, new_size, new_size / old_size])
        info = pd.DataFrame(size_list, columns=["FILE", "MEM_OLD", "MEM_NEW", "RATE"])

    def run(self):
        self._check()
        files = list(Path(f"{self.path_src}").glob("*.[jp][pn]g"))
        t_files = tqdm.tqdm(files)
        executor = ThreadPoolExecutor()

        futures = []
        for file in t_files:
            obj = executor.submit(self._core, file)
            futures.append(obj)

        for future in as_completed(futures):
            t_files.update(1)
            t_files.set_description(f"正在转换：{future.result()}")
        executor.shutdown()

        # self._get_report()

    def get_exif(self, path):
        """获取图片的EXIF信息
        相机厂商：tags['Image Make']
        相机型号：tags['Image Model']
        镜头型号：tags['EXIF LensModel']
        拍摄时间：tags['EXIF DateTimeOriginal']
        作者：tags['Image Artist']

        等效焦距：tags['EXIF FocalLengthIn35mmFilm']
        曝光时间：tags['EXIF ExposureTime']
        光圈大小：tags['EXIF FNumber']
        ISO：tags['EXIF ISOSpeedRatings']
        """
        with Path(path).open("rb") as f:
            tags = exifread.process_file(f)
        focal_length = tags["EXIF FocalLengthIn35mmFilm"]
        f_number = eval(str(tags["EXIF FNumber"]))
        exposure_time = tags["EXIF ExposureTime"]
        iso = tags["EXIF ISOSpeedRatings"]
        match self.camera_make:
            case "FujiFilm":
                cam_model = str(tags["Image Model"])
                lens_make = str(tags["EXIF LensMake"])
                logo = LOGO_CFG.LOGO_FUJIFILM
                logo_pure = LOGO_CFG.LOGO_FUJIFILM_PURE
            case "SONY":
                cam_model = str(tags["Image Software"]).split(" ")[0]
                lens_make = "SONY"
                logo = LOGO_CFG.LOGO_SONY
                logo_pure = LOGO_CFG.LOGO_SONY_PURE
            case _:
                msg = "相机型号不支持"
                raise KeyError(msg)
        lens_model = f'{lens_make}  {tags["EXIF LensModel"]}'
        date_format = "%Y:%m:%d %H:%M:%S"
        shot_time = datetime.strptime(str(tags["EXIF DateTimeOriginal"]), date_format)
        try:
            artist = str(tags["Image Artist"])
        except KeyError:
            artist = self.init_info["Image Artist"]

        img = Image.open(path).convert("RGBA")
        filename = os.path.split(path)[-1].split(".")[0]
        w, h, img = self._resize_img(img)

        exif = {
            "image": img,
            "filename": filename,
            "aim_size": self.aim_size,
            "path_dst": self.path_dst,
            "artist": artist,
            "width": w,
            "height": h,
            "focal_length": focal_length,
            "f_number": f_number,
            "exposure_time": exposure_time,
            "iso": iso,
            "cam_make": self.camera_make.lower(),
            "cam_model": cam_model,
            "lens_make": lens_make if lens_make not in lens_model else "",
            "lens_model": lens_model,
            "shot_time": shot_time,
            "logo": logo,
            "logo_pure": logo_pure,
        }
        return validate_exif(data=exif)

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
    for style in [
        # "MARK_0",
        # "MARK_1",
        # "MARK_2",
        # "MARK_3",
        # "MARK_4",
        # "MARK_5",
        "MARK_CONAN",
    ]:
        my_watermarker = KokoWaterMark(
            path_src=r"./src",
            path_dst=r"./dst",
            watermark_style=style,
            aim_size=1024,
        )
        my_watermarker.run()


if __name__ == "__main__":
    example()
