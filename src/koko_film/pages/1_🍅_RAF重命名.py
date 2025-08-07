"""
=========================================================================
@File Name: 1_🍅_RAF重命名.py
@Time: 2024/5/31 上午12:45
@Program IDE：PyCharm
@Create by Author: 一一风和橘
@Motto: "The trick, William Potter, is not minding that it hurts."
@Description:
- 🍅
-
=========================================================================
"""

import os
from pathlib import Path

import streamlit as st

from koko_film.common.base import PathBase
from koko_film.common.config import config
from koko_film.raf_tools.raf_archive import raf_archive
from koko_film.raf_tools.raf_renamer import raf_renamer
from koko_film.utils.page_init import page_init, page_md


def page_main(
    raf_src,
    raf_name,
    aim_model,
):
    # 移动、重命名
    raf_renamer(
        raf_src,
        config.APP.RAF_ROOT,
        aim_model,
        config.APP.MAX_WORKERS,
    )

    # 创建toml
    for folder in Path(config.APP.RAF_ROOT).iterdir():
        if Path(folder, "Archive.toml").is_file():
            continue
        raf_archive(folder, raf_name)


def page_compose():
    col1, col2 = st.columns([6, 4])
    with col1:
        raf_src = st.text_input(
            "RAF源路径",
            key="raf_src",
        )
        col11, col12 = st.columns(2)
        with col11:
            raf_dst = st.text_input(
                "RAF目标路径",
                value=config.APP.RAF_ROOT,
                key="raf_dst",
                disabled=True,
            )
        with col12:
            raf_name = st.text_input(
                "相册名",
                value="",
                key="raf_name",
            )
        aim_model = st.selectbox(
            "修改相机型号",
            options=[
                "",
                "X-T50",
                "X100VI",
                "X-T5",
                "X-H2",
                "X-H2s",
                "X-S20",
                "X-T30II",
                "X-E4",
            ],
            index=0,
        )

        col11, col12, _, _ = st.columns(4)
        with col11:
            if st.button("重命名RAF", key="raf_btn") and raf_src:
                with st.spinner("等待进程..."):
                    page_main(
                        raf_src,
                        raf_name,
                        aim_model,
                    )
                    st.success("重命名完成！")
        with col12:
            if st.button("打开文件路径"):
                os.startfile(raf_dst)

        contents = [
            "功能1：基于ExifTool读取RAF的创建日期，重命名文件。",
            "如：`DSCF0061.RAF`重命名为`20240721_DSCF0061.RAF`",
            "功能2：基于ExifTool修改相机信息，以支持在Capture One中解锁更多胶片模拟。",
            "如：原相机`X-T30`修改为`X-T50`，解锁`CLASSIC Neg`、`NOSTALGIC Neg`、`ETERNA BLEACH BYPASS`、`REALA ACE`",
        ]
        with st.expander("实现说明"):
            page_md(contents)


if __name__ == "__main__":
    page_init("RAF重命名", "🍅")
    page_compose()
