"""
=========================================================================
@File Name: compress.py
@Time: 2024/5/13 上午3:12
@Program IDE：PyCharm
@Create by Author: 一一风和橘
@Motto: "The trick, William Potter, is not minding that it hurts."
@Description:
-
-
=========================================================================
"""

import os
import subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

import pandas as pd
import tqdm
from PIL import Image

try:
    from ..config import CONFIG
except ImportError:
    from config import CONFIG


def __sub_compress_webp(img_name, path_src, path_dst, limit_size=500, limit_width=2560):
    aim_size = limit_size * 1024
    assert Path(CONFIG.PATH_CWEBP).exists(), "cwebp.exe is not found"
    cmd = (
        f'{CONFIG.PATH_CWEBP} -q {CONFIG.QUALITY_INIT} {path_src}/{img_name} -o '
        f'{path_dst}/{img_name.split(".")[0]}.'
        f'webp -m 6 -size {aim_size} -resize {limit_width} 0 -noalpha -quiet -jpeg_like'
    )
    process = subprocess.Popen(cmd, shell=True)
    process.wait()
    return img_name


def __sub_cut_cover(img_name, path_src, path_dst, limit_size=500, limit_width=2560, limit_height=853):
    filepath = f"{path_src}/{img_name}"
    filename = img_name.split(".")[0]
    old_size = Path(f"{path_src}/{img_name}").stat().st_size
    new_size = old_size
    quality = CONFIG.QUALITY_INIT
    img = Image.open(filepath)
    w = img.size[0]
    h = img.size[1]

    height = int(limit_width * h / w)
    img = img.resize((limit_width, height))
    x0 = 0
    y0 = int((height - limit_height) / 2)
    x1 = limit_width
    y1 = int((height + limit_height) / 2)
    img = img.crop((x0, y0, x1, y1))
    while new_size > limit_size * 1024:
        quality -= 5
        img.save(f"{path_dst}/{filename}.webp", "webp", quality=quality)
        new_size = Path(f"{path_dst}/{filename}.webp").stat().st_size
    return img_name


def compress_webp(
    path_src: str,
    path_dst: str,
    limit_size: int = 500,
    limit_width: int = 2560,
    max_workers: int = 12,
):
    """图片压缩为webp格式

    Parameters
    ----------
    path_src : str
        源文件夹
    path_dst : str
        目标文件夹
    limit_size : int
        限制大小
    limit_width : int
        限制宽度
    max_workers : int
        工作线程数

    Returns
    -------
    info : pd.DataFrame
        压缩信息

    Examples
    -------
    >>> res = compress_webp('./init', './webp')
    """
    files = os.listdir(path_src)
    t_files = tqdm.tqdm(files)
    files = [item for item in files if not Path(f"{path_src}/{item}").is_dir()]

    with ThreadPoolExecutor(max_workers=max_workers) as t:
        futures = [
            t.submit(
                __sub_compress_webp,
                file,
                path_src,
                path_dst,
                limit_size,
                limit_width,
            )
            for file in files
            if file != "Desktop.ini"
        ]

        for future in as_completed(futures):
            t_files.update(1)
            t_files.set_description(future.result())


def compress_cover(
    path_src: str,
    path_dst: str,
    limit_size: int = 500,
    limit_width: int = 2560,
    limit_height=1442,
    max_workers: int = 12,
):
    files = os.listdir(path_src)
    t_files = tqdm.tqdm(files)

    with ThreadPoolExecutor(max_workers=max_workers) as t:
        futures = [
            t.submit(
                __sub_cut_cover,
                file,
                path_src,
                path_dst,
                limit_size,
                limit_width,
                limit_height,
            )
            for file in files
            if file != "Desktop.ini"
        ]

        for future in as_completed(futures):
            t_files.update(1)
            t_files.set_description(future.result())

    size_list = []
    for file in files:
        old_size = Path(f"{path_src}/{file}").stat().st_size
        new_size = Path(f'{path_dst}/{file.split(".")[0]}.webp').stat().st_size
        size_list.append([file, old_size, new_size, new_size / old_size])
    return pd.DataFrame(size_list, columns=["FILE", "MEM_OLD", "MEM_NEW", "RATE"])


def compress_tinypng():
    pass


if __name__ == "__main__":
    compress_webp(
        "./src",
        "./dst",
    )
    # compress_cover(
    #     r"src",
    #     r"./dst",
    #     limit_size=400,
    #     limit_width=1280,
    #     limit_height=480,
    #     max_workers=8,
    # )
