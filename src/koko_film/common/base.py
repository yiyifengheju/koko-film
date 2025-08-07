"""
=========================================================================
@File Name: base.py
@Time: 2025/6/28 13:43
@Program IDE: PyCharm
@Create by Author: 一一风和橘
@Motto: "The trick, William Potter, is not minding that it hurts."
@Description:
-
-
=========================================================================
"""

import os
from dataclasses import dataclass
from pathlib import Path
from koko_film.common.config import config
import toml


@dataclass
class DictSummary:
    ALBUM: str = ""
    DATE: str = ""
    CAM_MODEL: str | list[str] = ""
    LENS_MODEL: str | list[str] = ""
    PROVINCE: str = ""
    CITY: str = ""
    DISTRICT: str = ""
    SCENIC_SPOT: str | list[str] = ""
    PERSON: str = ""
    TAGS: str | list[str] = ""
    ARCHIVED: str | list[str] = ""
    RANK: str = ""


@dataclass
class DictSync:
    NAS_SYNC: bool = False
    NAS_PATH: str = ""
    SYNC_DATE: str = ""


@dataclass
class DictImages:
    FILENAME: str = ""
    SHOT_TIME: str = ""
    INIT_SIZE: int = ""
    ARTIST: str = ""
    WIDTH: int = ""
    HEIGHT: int = ""
    FOCAL_LENGTH: str = ""
    F_NUMBER: str = ""
    EXPOSURE_TIME: str = ""
    ISO: str = ""
    CAM_MAKE: str = ""
    CAM_MODEL: str = ""
    LENS_MAKE: str = ""
    LENS_MODEL: str = ""
    PATH_RAF: str = ""
    PATH_JPG: list = ""
    PATH_WEBP: list = ""


@dataclass
class ArchToml:
    SUMMARY: DictSummary
    SYNC: DictSync
    IMAGES: dict[str, "DictImages"]


class PathBase:
    def __init__(self, root: str | Path):
        self.root = Path(config.APP.RAF_ROOT, root)
        self.toml = Path(config.APP.RAF_ROOT, root, "Archive.toml")
        self.raf = Path(config.APP.RAF_ROOT, root, "RAF")
        self.jpg = Path(config.APP.RAF_ROOT, root, "JPG")
        self.webp = Path(config.APP.RAF_ROOT, root, "WEBP")

    def init_dirs(self):
        for item in [self.raf, self.jpg, self.webp]:
            item.mkdir(parents=True, exist_ok=True)
        self.toml.touch(exist_ok=True)

    def update_toml(self, arch_toml):
        with self.toml.open(mode="w", encoding="utf-8") as f:
            toml.dump(f, arch_toml)


def koko_print(
    msg: str,
):
    if os.environ.get("CALLER_STACK") == "TYPER":
        import typer

        return typer.echo(msg)
    elif os.environ.get("CALLER_STACK") == "STREAMLIT":
        import streamlit as st

        return st.write(msg)
    else:
        return print(msg)


def koko_print_style(
    text: str,
    color_code=30,
    format_code=None,
):
    reset_code = "\033[0m"
    if format_code:
        msg = f"\033[{format_code};{color_code}m{text}{reset_code}"
    else:
        msg = f"\033[{color_code}m{text}{reset_code}"
    if os.environ.get("CALLER_STACK") == "TYPER":
        import typer

        return typer.echo(msg)
    elif os.environ.get("CALLER_STACK") == "STREAMLIT":
        import streamlit as st

        return st.write(msg)
    else:
        return print(msg)
