"""
=========================================================================
@File Name: raf_archive.py
@Time: 2025/6/18 23:15
@Program IDE: PyCharm
@Create by Author: 一一风和橘
@Motto: "The trick, William Potter, is not minding that it hurts."
@Description:
-
-
=========================================================================
"""

import subprocess
from dataclasses import asdict
from datetime import datetime
from functools import lru_cache
from pathlib import Path

import chardet
import toml

from koko_film.common.base import (
    ArchToml,
    DictImages,
    DictSummary,
    DictSync,
    PathBase,
    koko_print,
)
from koko_film.common.config import config


@lru_cache(maxsize=128)
def get_exif(img_path: Path) -> DictImages:
    cmd = [config.BIN.EXIFTOOL, img_path]
    try:
        raw = subprocess.check_output(cmd, shell=True, cwd="./")
        encoding = chardet.detect(raw)["encoding"]
        result = raw.decode(encoding or "utf-8", errors="ignore")
        result.strip()
    except subprocess.CalledProcessError as e:
        koko_print(str(e))
        assert 0
    tags = {}
    for line in result.splitlines():
        try:
            line = line.strip().split(": ")
            tags[line[0].strip()] = line[1].strip()
        except IndexError:
            continue
    date_format = "%Y:%m:%d %H:%M:%S"

    return DictImages(
        FILENAME=tags["File Name"].split(".")[0],
        SHOT_TIME=datetime.strptime(
            tags["Date/Time Original"].replace("+08:00", ""),
            date_format,
        ).strftime("%Y.%m.%d %H:%M:%S"),
        INIT_SIZE=int(float(tags["File Size"].replace(" MB", "")) * 1024),
        ARTIST=tags.get("Artist", "ARTMALLO"),
        WIDTH=int(tags["Image Width"]),
        HEIGHT=int(tags["Image Height"]),
        FOCAL_LENGTH=tags["Focal Length In 35mm Format"],
        F_NUMBER=tags["F Number"],
        EXPOSURE_TIME=tags["Exposure Time"],
        ISO=tags["ISO"],
        CAM_MAKE=tags["Make"],
        CAM_MODEL=tags["Camera Model Name"],
        LENS_MAKE=tags["Lens Make"],
        LENS_MODEL=tags["Lens Model"],
        PATH_RAF=img_path.relative_to(config.APP.RAF_ROOT).as_posix(),
        PATH_JPG=[],
        PATH_WEBP=[],
    )


def raf_archive(
    path_root: str | Path | PathBase,
    raf_name: str,
) -> None:
    if isinstance(path_root, PathBase):
        path_cls = path_root
    elif isinstance(path_root, Path):
        path_cls = PathBase(Path(config.APP.RAF_ROOT, path_root))
    elif isinstance(path_root, str) and Path(path_root).is_dir():
        path_cls = PathBase(path_root)
    elif isinstance(path_root, str) and Path(config.APP.RAF_ROOT, path_root).is_dir():
        path_cls = PathBase(Path(config.APP.RAF_ROOT, path_root))
    else:
        raise TypeError("输入路径格式错误")
    path_cls.init_dirs()
    arch_info = ArchToml(
        SUMMARY=DictSummary(
            ALBUM=raf_name,
            DATE=path_cls.root.name,
        ),
        SYNC=DictSync(),
        IMAGES={},
    )

    cams, lens = [], []
    jpgs = [item.name for item in path_cls.jpg.iterdir()]
    webps = [item.name for item in path_cls.webp.iterdir()]
    # spinner = Halo(text="", spinner=spinner_type)
    # spinner.start()
    for file in path_cls.raf.iterdir():
        if file.suffix == ".RAF":
            print(file)
            info = get_exif(file)
            cams.append(info.CAM_MODEL)
            lens.append(info.LENS_MODEL)
            jpg_tmp = [item for item in jpgs if item.startswith(info.FILENAME)]
            webp_tmp = [item for item in webps if item.startswith(info.FILENAME)]
            info.PATH_JPG = jpg_tmp
            info.PATH_WEBP = webp_tmp
            arch_info.IMAGES[info.FILENAME] = info
            msg = (
                f"📷  {file.name} ==> "
                f"{info.LENS_MAKE} "
                f"{info.LENS_MODEL}, "
                f"{info.FOCAL_LENGTH}mm "
                f"f/{info.F_NUMBER} "
                f"{info.EXPOSURE_TIME} "
                f"ISO{info.ISO} ==> "
                f"JPG: {len(info.PATH_JPG)}"
            )
            # spinner.text = msg
            koko_print(msg)
    arch_info.SUMMARY.CAM_MODEL = list(set(cams))
    arch_info.SUMMARY.LENS_MODEL = list(set(lens))
    msg = f"🎉  {path_cls.root.as_posix()} 归档完成"
    koko_print(msg)
    # spinner.stop_and_persist(symbol="🎉 ", text=f"{path_cls.root.as_posix()} 归档完成")
    with path_cls.toml.open(mode="w", encoding="utf-8") as f:
        toml.dump(asdict(arch_info), f)


if __name__ == "__main__":
    PATH_RAF = Path(r"H:\200_RAF")
    for path in PATH_RAF.iterdir():
        path = r"H:\DAOCHU\20230513"
        raf_archive(path)
        assert 0
