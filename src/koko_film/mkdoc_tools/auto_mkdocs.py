"""
=========================================================================
@File Name: auto_mkdocs.py
@Time: 2024/8/5 上午12:21
@Program IDE：PyCharm
@Create by Author: 一一风和橘
@Motto: "The trick, William Potter, is not minding that it hurts."
@Description:
-
-
=========================================================================
"""

import hashlib
import os
import random
import shutil
import subprocess
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import exifread
import pandas as pd
import tqdm

from PyPulse.base import ENV


class LOGO:
    FujiFilm = "https://cdn.jsdelivr.net/gh/yiyifengheju/picbed@main/sources/Fujifilm.svg"


class AutoMkdocs:
    def __init__(
        self,
        path_src,
        path_dst,
        limit_size=500,
        limit_width=2560,
        max_workers=12,
    ):
        self.path_src = path_src
        self.title = os.path.split(path_src)[-1]
        if path_dst is None:
            self.path_dst = f"{path_src}/0_WebP"
        else:
            self.path_dst = path_dst
        if not Path(f"{self.path_dst}/{self.title}").exists():
            Path(f"{self.path_dst}/{self.title}").mkdir(parents=True, exist_ok=True)

        self.limit_size = limit_size
        self.width_limit = limit_width
        self.path_logo = LOGO.FujiFilm

        self.obj_list = []
        self.executor = ThreadPoolExecutor(max_workers=max_workers)
        self.compress_res = []
        self.compress_rate_all = None
        self.head = ["---\n", f"title: {self.title}\n", "comments: true\n", "hide:\n", "  - toc\n", "---\n\n"]
        self.tail = ['<div class="shot-info">\n', "\n", "<br>\n", "\n", "</div>\n"]
        self.html = {}

    def run(self, *, is_auto=True):
        # 第0步，重命名
        files = os.listdir(self.path_src)
        for file in files:
            new_file = file.replace(" ", "")
            Path(f"{self.path_src}/{file}").rename(f"{self.path_src}/{new_file}")

        # 第一步，压缩图片
        files = os.listdir(self.path_src)
        for item in files:
            if item == "0_WebP":
                continue

            obj = self.executor.submit(self.compress_image, item)
            self.obj_list.append(obj)

        # 第二步，停止接受新的任务，等待任务完成，统计结果
        self.executor.shutdown()
        for obj in self.obj_list:
            res = obj.result()
            self.compress_res.append(res)
        self.compress_res = pd.DataFrame(self.compress_res)
        self.compress_res.columns = ["Filename", "原始大小/kb", "压缩大小/kb", "压缩比"]
        self.compress_rate_all = self.compress_res["压缩大小/kb"].mean() / self.compress_res["原始大小/kb"].mean()

        if is_auto:
            # 第三步，生成Markdown
            self.generate_md()

    def get_webp_path(self):
        md5_hash = hashlib.md5()
        md5_hash.update(self.title.encode("utf-8"))
        path = rf"{self.path_dst}\{md5_hash.hexdigest()[:8]}"
        if not Path(path).exists():
            Path(path).mkdir(parents=True, exist_ok=True)
        else:
            shutil.rmtree(path)
            os.mkdir(path)
        return md5_hash.hexdigest()[:8]

    def compress_image(self, img_name):
        aim_size = self.limit_size * 1024
        cmd = (
            f'{ENV.CWEBP} -q {ENV.QUALITY_INIT} {self.path_src}/{img_name} -o '
            f'{self.path_dst}/{self.title}/{img_name.split(".")[0]}.webp'
            f' -m 6 -size {aim_size} -resize {self.width_limit} 0 -noalpha -quiet -jpeg_like'
        )
        process = subprocess.Popen(cmd, shell=True)
        process.wait()
        old_size = os.path.getsize(rf"{self.path_src}/{img_name}")
        new_size = os.path.getsize(rf'{self.path_dst}/{self.title}/{img_name.split(".")[0]}.webp')
        return img_name, old_size, new_size, new_size / old_size

    def generate_md(self, wall_1_list=None, wall_2_list=None):
        if wall_1_list == "":
            wall_1_list = None
        if wall_2_list == "":
            wall_2_list = None
        wall_all = wall_1_list + wall_2_list
        # 获取图片列表
        img_list = os.listdir(f"{self.path_dst}/{self.title}")
        t_img_list = tqdm.tqdm(img_list)
        for img in t_img_list:
            if img == "0_WebP":
                continue
            if img[-2:] == "md":
                continue
            if img not in wall_all:
                os.remove(f"{self.path_dst}/{self.title}/{img}")
            t_img_list.set_description(f"{img}")
            self.html[img] = []

            # 读取文件EXIF信息
            path = f"{self.path_src}/{img[:-5]}.jpg"
            try:
                with open(path, "rb") as f:
                    tags = exifread.process_file(f)
            except FileNotFoundError:
                continue
            try:
                camera_model = str(tags["Image Model"])
                focal_length = tags["EXIF FocalLengthIn35mmFilm"]
                f_number = eval(str(tags["EXIF FNumber"]))
                exposure_time = tags["EXIF ExposureTime"]
                iso = tags["EXIF ISOSpeedRatings"]

                lens_make = tags["EXIF LensMake"]
                lens_model = tags["EXIF LensModel"]
            except KeyError:
                print(img)
                assert 0

            # 生成图片html
            name = "s" + img.split(".")[0]
            tmp = (
                f'<div class="photo"><img alt="{name}" class="thumb" '
                f'data-description=".{name}" '
                f'src="https://cdn.jsdelivr.net/gh/yiyifengheju/picbed@main/{self.title}/low-{img}" '
                f'data-lazy-src="https://cdn.jsdelivr.net/gh/yiyifengheju/picbed@main/{self.title}/{img}"></div>\n'
            )
            self.html[img].append(tmp)

            # 生成水印html
            tmp = [
                f'<div class="glightbox-desc {name}">',
                '<div class="pre-msg">',
                f'<div class="shot-model">{camera_model}</div>\n',
                '<div class="descript"></div> ',
                "</div>",
                '<div class="kong"></div>',
                '<div class="shot-logo"></div>',
                '<div class="vertical-line"></div>',
                '<div class="msg">',
                f'<div class="lens-param">{focal_length}mm  f/{f_number:.1f}  {exposure_time}s  ISO{iso}</div>',
                f'<div class="lens">{lens_make} {lens_model}</div>',
                "</div></div>",
                "\n\n",
            ]
            self.html[img].extend(tmp)

        if wall_1_list is None and wall_2_list is None:
            random.shuffle(img_list)
            self.head.append('<div class="photo-wall">\n')
            for img in img_list:
                self.head.extend(self.html[img])
            self.head.append("</div>")
        else:
            if wall_1_list is not None:
                self.head.append('<div class="photo-wall-1">\n')
                for img in wall_1_list:
                    self.head.extend(self.html[img])
                self.head.append("</div>")
            if wall_2_list is not None:
                self.head.append('<div class="photo-wall">\n')
                for img in wall_2_list:
                    self.head.extend(self.html[img])
                self.head.append("</div>")

        with open(f"{self.path_dst}/{self.title}.md", "w", encoding="utf-8") as f:
            f.writelines(self.head)
            f.writelines(self.tail)
        return 0


if __name__ == "__main__":
    paths = [
        # r'C:\Users\Artmallo\Desktop\20240707',
        #      r'C:\Users\Artmallo\Desktop\20231230',
        #      r'C:\Users\Artmallo\Desktop\20240713',
        #      r'C:\Users\Artmallo\Desktop\20240716',
        #      r'C:\Users\Artmallo\Desktop\20240623',
        #      r'C:\Users\Artmallo\Desktop\202407132',
        #      r'C:\Users\Artmallo\Desktop\20240526',
        r"C:\Users\Artmallo\Desktop\20240721",
    ]

    for src in paths:
        am = AutoMkdocs(
            path_src=src,
        )
        am.run()
