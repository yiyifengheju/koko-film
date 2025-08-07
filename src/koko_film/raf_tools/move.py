"""
=========================================================================
@File Name: move.py
@Time: 2025/7/5 20:51
@Program IDE: PyCharm
@Create by Author: 一一风和橘
@Motto: "The trick, William Potter, is not minding that it hurts."
@Description:
-
-
=========================================================================
"""

import shutil
from pathlib import Path


def move_pics():
    path_src = r"H:\桌面\仿coco"
    path_dst = r"H:\200_RAF"
    files = Path(path_src).iterdir()
    for file in files:
        folder = file.name.split("_D")[0]
        Path(path_dst, folder, "JPG").mkdir(parents=True, exist_ok=True)
        name = file.name
        if Path(path_dst, folder, "JPG", file.name).exists():
            print(file.name)
            for i in range(1, 10):
                name = file.name.split(".")[0] + f"_{i}.jpg"
                if not Path(path_dst, folder, "JPG", file.name).exists():
                    break
        shutil.copy(file, Path(path_dst, folder, "JPG", name))


def get_folders():
    path_src = r"H:\DAOCHU"
    path_dst = r"H:\200_RAF"
    folders0 = Path(path_dst).iterdir()
    folders0 = [item.name for item in folders0]
    folders = Path(path_src).iterdir()
    for folder in folders:
        if folder.name not in folders0:
            print(folder.name)


def move_picss():
    path_src = r"H:\桌面\cover"
    path_dst = r"H:\200_RAF"
    folders = Path(path_src).iterdir()
    for folder in folders:
        for jpg in folder.iterdir():
            if jpg.name == "0_WebP":
                continue
            name = jpg.name
            Path(path_dst, folder.name, "JPG").mkdir(parents=True, exist_ok=True)
            if Path(path_dst, folder.name, "JPG", jpg.name).exists():
                print(folder.name, jpg.name)
                for i in range(1, 10):
                    name = jpg.name.split(".")[0] + f"_{i}.jpg"
                    if not Path(path_dst, folder.name, "JPG", jpg.name).exists():
                        break
            shutil.copy(jpg, Path(path_dst, folder.name, "JPG", name))


if __name__ == "__main__":
    move_pics()
