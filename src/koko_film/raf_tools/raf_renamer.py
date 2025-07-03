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
import subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

import tqdm

from koko_film.common.config import config

bin_exiftool = Path(config.BIN.EXIFTOOL).absolute()


def run_cmd(cmd, cwd):
    try:
        result = subprocess.check_output(
            cmd,
            shell=True,
            cwd=cwd,
            text=False,
            encoding="utf-8",
        )
        return result.strip()
    except subprocess.CalledProcessError as e:
        print(e)


def run(file, path_src, path_dst, aim_model):
    raf_path = Path(path_src, file).absolute()
    # fmt: off
    if aim_model:
        cmd = (f'{bin_exiftool} '
               f'"-Model={aim_model}" '
               # f'"-Software=Digital Camera {aim_model} Ver1.00" '
               f'"-FileName<CreateDate" -d "{path_dst}/%Y%m%d/%Y%m%d_%%f.%%e" '
               f'"{raf_path}"')
    else:
        cmd = (f'{bin_exiftool} '
               f'"-FileName<CreateDate" -d "{path_dst}/%Y%m%d/%Y%m%d_%%f.%%e" '
               f'"{raf_path}"')
    # fmt: on
    run_cmd(cmd, "./")


def raf_renamer(
    path_src: str,
    path_dst: str,
    aim_model: str,
    max_workers: int = config.APP.MAX_WORKERS,
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
    assert Path(config.BIN.EXIFTOOL).exists(), "exiftool.exe is not found"

    Path(path_dst).mkdir(parents=True, exist_ok=True)

    files = os.listdir(path_src)
    t_file_list = tqdm.tqdm(files)

    with ThreadPoolExecutor(max_workers=max_workers) as t:
        futures = [
            t.submit(run, file, path_src, path_dst, aim_model)
            for file in files
            if file != "Desktop.ini"
        ]
        for future in as_completed(futures):
            t_file_list.update(1)
            t_file_list.set_description(future.result())


if __name__ == "__main__":
    src = r"C:\Users\mastermao\Desktop\dcim"
    dst = r"C:\Users\mastermao\Desktop\RAF"
    raf_renamer(src, dst, aim_model="")
