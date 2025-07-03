"""
=========================================================================
@File Name: config.py
@Time: 2025/6/28 12:53
@Program IDE: PyCharm
@Create by Author: 一一风和橘
@Motto: "The trick, William Potter, is not minding that it hurts."
@Description:
-
-
=========================================================================
"""

import os
from pathlib import Path

import toml
from pydantic import BaseModel

DEFAULT_CONFIG = Path(__file__).parent / "config.toml"


class VersionCFG(BaseModel):
    VERSION: str
    AUTHOR: str


class BinCFG(BaseModel):
    CWEBP: str
    EXIFTOOL: str


class FontsCFG(BaseModel):
    LATO: str
    MONACO: str
    MPLUS: str
    NOTO_JP: str
    NOTO_SC: str


class LogoCFG(BaseModel):
    FUJIFILM: str
    FUJIFILM_PURE: str
    SONY: str
    SONY_PURE: str


class AppCFG(BaseModel):
    THEME: str
    QUALITY_INIT: int
    MAX_WORKERS: int
    RAF_ROOT: str
    CALLER_STACK: str


class CONFIG(BaseModel):
    VERSION: VersionCFG
    BIN: BinCFG
    LOGO: LogoCFG
    FONTS: FontsCFG
    APP: AppCFG

    @classmethod
    def from_toml(
        cls,
        path_toml: str | Path = None,
    ) -> "CONFIG":
        path_toml = Path(path_toml) if path_toml else DEFAULT_CONFIG
        config_data = toml.load(path_toml)
        config_base_dir = path_toml.parent
        processed_data = cls._resolve_relative_paths(config_data, config_base_dir)
        return cls(**processed_data)

    @classmethod
    def _resolve_relative_paths(cls, config_data: dict, base_dir: Path) -> dict:
        """递归处理配置中的相对路径"""
        processed = {}

        for key, value in config_data.items():
            if isinstance(value, str):
                if not os.path.isabs(value) and any(
                    sep in value for sep in ["/", "\\"]
                ):
                    try:
                        resolved = (base_dir / value).resolve()
                        processed[key] = str(resolved)
                    except Exception:
                        processed[key] = value
                else:
                    processed[key] = value

            elif isinstance(value, list):
                new_list = []
                for item in value:
                    if (
                        isinstance(item, str)
                        and not os.path.isabs(item)
                        and any(sep in item for sep in ["/", "\\"])
                    ):
                        try:
                            resolved = (base_dir / item).resolve()
                            new_list.append(str(resolved))
                        except Exception:
                            new_list.append(item)
                    else:
                        new_list.append(item)
                processed[key] = new_list

            elif isinstance(value, dict):
                processed[key] = cls._resolve_relative_paths(value, base_dir)

            else:
                processed[key] = value

        return processed


config = CONFIG.from_toml()
config.APP.CALLER_STACK = os.environ.get("CALLER_STACK")
spinner_type = {"interval": 80, "frames": ["⣾", "⣽", "⣻", "⢿", "⡿", "⣟", "⣯", "⣷"]}

