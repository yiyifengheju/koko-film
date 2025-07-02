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
from koko_film.common.base import PathArchiveCls


from koko_film.koko_marker.sub_marker_1 import sub_marker_1
from koko_film.koko_marker.sub_marker_2 import sub_marker_2
from koko_film.koko_marker.sub_marker_3 import sub_marker_3
from koko_film.koko_marker.sub_marker_4 import sub_marker_4
from koko_film.koko_marker.sub_marker_5 import sub_marker_5
from koko_film.koko_marker.sub_marker_6 import sub_marker_conan
from koko_film.common.config import config
from koko_film.koko_marker.base import MarkerEXIF, validate_exif


class Marker:
    def __init__(
        self,
        marker_exif: MarkerEXIF,
    ):
        self.marker_exif = marker_exif

    def run(
        self,
        style: str,
        aim_size: float,
    ):
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

        quality = config.APP.QUALITY_INIT
        file_path = Path(
            self.marker_exif.PATH_DST, f"{self.marker_exif.FILENAME}_{style}.webp"
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
        path_root: str,
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
            "ALL"
        ] = "ALL",
    ):
        self.aim_width = aim_width
        self.aim_size = aim_size
        self.watermark_style = watermark_style
        self.path_marker = PathArchiveCls(path_root)

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
        files = Path(self.path_marker.jpg).glob("*.[jp][pn]g")
        num_tasks = len(list(files))
        pbar = tqdm.tqdm(total=num_tasks)
        def update_progress(future):
            pbar.update(1)

        with ThreadPoolExecutor(max_workers=12) as executor:
            futures = [executor.submit(self._core, file) for file in files]
            for future in futures:
                future.add_done_callback(update_progress)

    def run_single(self):
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

    def get_exif(self, path:Path):
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
        with path.open("rb") as f:
            tags = exifread.process_file(f)
        focal_length = tags.get("EXIF FocalLengthIn35mmFilm")
        f_number = eval(tags.get("EXIF FNumber"))
        exposure_time = tags.get("EXIF ExposureTime")
        iso = tags.get("EXIF ISOSpeedRatings")
        cam_model = tags.get("Image Model")
        lens_make = tags["EXIF LensMake"]
        logo = config.LOGO.FUJIFILM
        logo_pure = config.LOGO.FUJIFILM_PURE
        lens_model = f'{lens_make}  {tags.get("EXIF LensModel")}'
        date_format = "%Y:%m:%d %H:%M:%S"
        shot_time = datetime.strptime(str(tags.get("EXIF DateTimeOriginal")), date_format)
        try:
            artist = tags.get("Image Artist")
        except KeyError:
            artist = "Artmallo"

        img = Image.open(path).convert("RGBA")
        filename = path.name.split(".")[0]
        w, h, img = self._resize_img(img)

        exif = {
            "IMAGE": img,
            "FILENAME": filename,
            "AIM_SIZE": self.aim_size,
            "PATH_DST": self.path_marker.webp,
            "ARTIST": artist,
            "WIDTH": w,
            "HEIGHT": h,
            "FOCAL_LENGTH": focal_length,
            "F_NUMBER": f_number,
            "EXPOSURE_TIME": exposure_time,
            "ISO": iso,
            "CAM_MAKE": "fujifilm",
            "CAM_MODEL": cam_model,
            "LENS_MAKE": lens_make if lens_make not in lens_model else "",
            "LENS_MODEL": lens_model,
            "SHOT_TIME": shot_time,
            "LOGO": logo,
            "LOGO_PURE": logo_pure,
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
    my_watermarker = KokoWaterMark(
        path_root=r"H:\200_RAF\20250608",
        aim_size=1024,
    )
    my_watermarker.run()


if __name__ == "__main__":
    example()
