"""
=========================================================================
@File Name: raf_renamer.py
@Time: 2024/5/13 上午2:09
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
from pathlib import Path

import tqdm

try:
    from ..config import CONFIG
except ImportError:
    from config import CONFIG


def __run(file, path_src, path_dst, aim_model):
    raf_path = Path(path_src, file).absolute()
    # fmt: off
    if aim_model:
        cmd = (f'{CONFIG.PATH_EXIFTOOL} '
               f'"-Model={aim_model}" '
               # f'"-Software=Digital Camera {aim_model} Ver1.00" '
               f'"-FileName<CreateDate" -d "{path_dst}/%Y%m%d/%Y%m%d_%%f.%%e" '
               f'"{raf_path}"')
    else:
        cmd = (f'{CONFIG.PATH_EXIFTOOL} '
               f'"-FileName<CreateDate" -d "{path_dst}/%Y%m%d/%Y%m%d_%%f.%%e" '
               f'"{raf_path}"')
    # fmt: on
    os.popen(cmd)


def raf_renamer(
    path_src: str,
    path_dst: str,
    aim_model: str,
    max_workers: int = CONFIG.MAX_WORKERS,
) -> None:
    """RAF文件重命名和归档

    Parameters
    ----------
    path_src : str
        源路径
    path_dst : str
        目标路径
    aim_model : str
        目标相机型号
    max_workers : int
        最大工作线程，默认12

    Returns
    -------
    None

    """
    assert Path(CONFIG.PATH_EXIFTOOL).exists(), "exiftool.exe is not found"

    if not Path(path_dst).exists():
        Path(path_dst).mkdir(parents=True, exist_ok=True)

    files = os.listdir(path_src)
    t_file_list = tqdm.tqdm(files)

    with ThreadPoolExecutor(max_workers=max_workers) as t:
        futures = [t.submit(__run, file, path_src, path_dst, aim_model) for file in files if file != "Desktop.ini"]
        for future in as_completed(futures):
            t_file_list.update(1)
            t_file_list.set_description(future.result())


if __name__ == "__main__":
    src = r"H:\桌面\未分类\xazq"
    dst = r"H:\DAOCHU"
    raf_renamer(src, dst, aim_model="")
