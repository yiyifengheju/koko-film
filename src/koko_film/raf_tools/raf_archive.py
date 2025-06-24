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
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path

import toml

try:
    from config import BIN_CFG
except ImportError:
    from koko_film.koko_marker.config import BIN_CFG
from halo import Halo

exiftool = Path(BIN_CFG.PATH_EXIFTOOL).absolute()
spinner_type = {"interval": 80, "frames": ["⣾", "⣽", "⣻", "⢿", "⡿", "⣟", "⣯", "⣷"]}


@dataclass
class KokoImages:
    FILENAME: str
    SHOT_TIME: str
    PATH_RAF: str
    PATH_JPG: list
    PATH_WEBP: list
    CAM_MAKE: str
    CAM_MODEL: str
    LENS_MAKE: str
    LENS_MODEL: str
    FOCAL_LENGTH: str
    F_NUMBER: str
    EXPOSURE_TIME: str
    ISO: str


class PathConfig:
    def __init__(self, root: str):
        self.root = Path(root)
        self.toml = Path(root, self.root.name + ".toml")
        self.raf = Path(root, "RAF")
        self.jpg = Path(root, "JPG")
        self.webp = Path(root, "WEBP")
        for item in [self.raf, self.jpg, self.webp]:
            if not item.exists():
                item.mkdir(parents=True, exist_ok=True)
        if not self.toml.exists():
            with self.toml.open(mode="w", encoding="utf-8") as f:
                toml.dump(template_toml(), f)


def template_toml():
    contents = {
        "SUMMARY": {
            "DATE": "N/A",
            "CAM_MODEL": "N/A",
            "LENS_MODEL": "N/A",
            "PROVINCE": "N/A",
            "CITY": "N/A",
            "DISTRICT": "N/A",
            "SCENIC_SPOT": "N/A",
            "PERSON": "N/A",
            "TAGS": "N/A",
            "ARCHIVED": "N/A",
            "RANK": "N/A",
        },
        "SYNC": {
            "NAS_SYNC": False,
            "NAS_PATH": "N/A",
        },
        "IMAGES": {},
    }
    return contents


def get_exif(img_path: Path) -> KokoImages:
    try:
        result = subprocess.check_output(
            f"{exiftool} {img_path}",
            shell=True,
            cwd="./",
            text=False,
            encoding="utf-8",
        )
        result.strip()
    except subprocess.CalledProcessError as e:
        print(e)
        assert 0
    tags = {}
    for line in result.splitlines():
        try:
            line = line.strip().split(": ")
            tags[line[0].strip()] = line[1].strip()
        except IndexError:
            continue
    date_format = "%Y:%m:%d %H:%M:%S"

    return KokoImages(
        FILENAME=str(tags["File Name"]).split(".")[0],
        PATH_RAF=str(img_path),
        PATH_JPG=[],
        PATH_WEBP=[],
        FOCAL_LENGTH=str(tags["Focal Length In 35mm Format"]),
        F_NUMBER=str(tags["F Number"]),
        EXPOSURE_TIME=str(tags["Exposure Time"]),
        ISO=str(tags["ISO"]),
        CAM_MAKE=tags["Make"],
        CAM_MODEL=str(tags["Camera Model Name"]),
        LENS_MAKE=str(tags["Lens Make"]),
        LENS_MODEL=str(tags["Lens Model"]),
        SHOT_TIME=datetime.strptime(
            str(tags["Date/Time Original"]).replace("+08:00", ""), date_format
        ).strftime("%Y.%m.%d %H:%M:%S"),
    )


def raf_archive(path_cfg):
    path_cfg = PathConfig(path_cfg)
    raf_toml = toml.load(path_cfg.toml)
    raf_toml["SUMMARY"]["DATE"] = str(path_cfg.root.name)
    cams, lens = [], []
    jpgs = [item.name for item in path_cfg.jpg.iterdir()]
    webps = [item.name for item in path_cfg.webp.iterdir()]
    spinner = Halo(text="", spinner=spinner_type)
    spinner.start()
    for file in path_cfg.raf.iterdir():
        spinner.text = file.name
        if file.suffix == ".RAF":
            info = get_exif(file)
            raf_toml["IMAGES"][info.FILENAME] = asdict(info)
            cams.append(info.CAM_MODEL)
            lens.append(info.LENS_MODEL)
            jpg_tmp = [item for item in jpgs if item.startswith(info.FILENAME)]
            webp_tmp = [item for item in webps if item.startswith(info.FILENAME)]
            raf_toml["IMAGES"][info.FILENAME]["PATH_JPG"] = jpg_tmp
            raf_toml["IMAGES"][info.FILENAME]["PATH_WEBP"] = webp_tmp
            raf_toml["SUMMARY"]["CAM_MODEL"] = list(set(cams))
            raf_toml["SUMMARY"]["LENS_MODEL"] = list(set(lens))
    spinner.text = ""
    spinner.stop_and_persist(symbol="🎉 ", text=f"{path_cfg} 归档完成")
    with path_cfg.toml.open(mode="w", encoding="utf-8") as f:
        toml.dump(raf_toml, f)


if __name__ == "__main__":
    PATH_RAF = Path(r"H:\200_RAF")
    for path in PATH_RAF.iterdir():
        raf_archive(path)
