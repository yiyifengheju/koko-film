"""
=========================================================================
@File Name: config.py
@Time: 2024/5/13 上午2:55
@Program IDE：PyCharm
@Create by Author: 一一风和橘
@Motto: "The trick, William Potter, is not minding that it hurts."
@Description:
-
-
=========================================================================
"""

from pathlib import Path

import toml
from pydantic import BaseModel


class VersionCFG(BaseModel):
    VERSION: str
    AUTHOR: str


class BinCFG(BaseModel):
    PATH_CWEBP: str
    PATH_EXIFTOOL: str


class FontsCFG(BaseModel):
    FONT_LATO: str
    FONT_MONACO: str
    FONT_MPLUS: str
    FONT_NOTO_JP: str
    FONT_NOTO_SC: str


class LogoCFG(BaseModel):
    LOGO_FUJIFILM: str
    LOGO_FUJIFILM_PURE: str
    LOGO_SONY: str
    LOGO_SONY_PURE: str


class AppCFG(BaseModel):
    THEME: str
    QUALITY_INIT: int
    MAX_WORKERS: int


try:
    with Path("./config.toml").open("r", encoding="utf-8") as f:
        config_dict = toml.load(f)
except FileNotFoundError:
    with Path(r"H:\600_PycharmProjects\koko-learn\src\koko_film\config.toml").open("r", encoding="utf-8") as f:
        config_dict = toml.load(f)

VERSION_CFG = VersionCFG(**config_dict["VERSION_CFG"])
BIN_CFG = BinCFG(**config_dict["BIN_CFG"])
FONTS_CFG = FontsCFG(**config_dict["FONTS_CFG"])
LOGO_CFG = LogoCFG(**config_dict["LOGO_CFG"])
APP_CFG = AppCFG(**config_dict["APP_CFG"])
