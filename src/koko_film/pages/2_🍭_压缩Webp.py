"""
=========================================================================
@File Name: 2_🍭_压缩Webp.py
@Time: 2024/5/19 上午1:38
@Program IDE：PyCharm
@Create by Author: 一一风和橘
@Motto: "The trick, William Potter, is not minding that it hurts."
@Description:
-
-
=========================================================================
"""

import os
from pathlib import Path

import streamlit as st

from koko_film.common.config import config
from koko_film.pic_tools import compress_cover, compress_webp
from koko_film.utils.page_init import page_init, page_md


def get_compress_info(path_src, path_dst, pre):
    import pandas as pd

    files = os.listdir(path_src)
    size_list = []
    for file in files:
        if Path(path_src, file).is_dir():
            continue
        old_size = Path(path_src, file).stat().st_size
        new_size = Path(path_dst, f"{file.split('.')[0]}.webp").stat().st_size
        Path(f'{path_dst}/{file.split(".")[0]}.webp').rename(
            f'{path_dst}/{pre}{"-" if pre else ""}{file.split(".")[0]}.webp',
        )
        size_list.append([file, old_size, new_size, new_size / old_size])
    return pd.DataFrame(size_list, columns=["FILE", "MEM_OLD", "MEM_NEW", "RATE"])


def page_main_1():
    st.markdown("## 图片压缩")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        limit_size = st.text_input(
            "限制大小/kb",
            key="limit_size",
            value="500",
        )
    with col2:
        limit_width = st.text_input(
            "限制宽度/px",
            key="limit_width",
            value="2560",
        )
    with col3:
        max_workers = st.selectbox(
            "工作核心数",
            (
                str(config.APP.MAX_WORKERS),
                str(config.APP.MAX_WORKERS // 2),
                str(config.APP.MAX_WORKERS // 4),
            ),
            index=0,
            key="max_workers",
        )
    with col4:
        rename_pre = st.text_input(
            "重命名",
            key="rename_pre",
            value="",
        )

    img_src = st.text_input(
        "IMG_SRC",
        key="img_src",
    )

    if st.button("压缩Webp", key="img_btn") and img_src:
        # tmp = os.path.abspath(os.path.join(img_src, os.pardir))
        tmp = Path(img_src).absolute()
        img_dst = f"{tmp}/2_WEBP"
        if not Path(img_dst).exists():
            Path(img_dst).mkdir(parents=True, exist_ok=True)

        with st.spinner("等待进程..."):
            compress_webp(
                img_src,
                img_dst,
                limit_size=eval(limit_size),
                limit_width=eval(limit_width),
                max_workers=eval(max_workers),
            )
            st.success("压缩完成！")
        info = get_compress_info(img_src, img_dst, rename_pre)
        with st.expander("压缩信息"):
            st.write(info)


def page_main_2():
    st.markdown("## 封面压缩")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        limit_size_2 = st.text_input(
            "限制大小/kb",
            key="limit_size_2",
            value="500",
        )
    with col2:
        limit_width_2 = st.text_input(
            "限制宽度/px",
            key="limit_width_2",
            value="2560",
        )
    with col3:
        limit_height_2 = st.text_input(
            "限制高度/px",
            key="limit_height_2",
            value="853",
        )
    with col4:
        max_workers_2 = st.selectbox(
            "工作核心数",
            (
                str(config.APP.MAX_WORKERS),
                str(config.APP.MAX_WORKERS // 2),
                str(config.APP.MAX_WORKERS // 4),
            ),
            index=0,
            key="max_workers_2",
        )

    img_src_2 = st.text_input(
        "IMG_SRC",
        key="img_src_2",
    )

    if st.button("压缩封面Webp", key="img_btn_2") and img_src_2:
        tmp = Path(img_src_2, os.pardir).absolute()
        img_dst_2 = f"{tmp}/3_COVER_WEBP"
        if not Path(img_dst_2).exists():
            Path(img_dst_2).mkdir(parents=True, exist_ok=True)

        with st.spinner("等待进程..."):
            info = compress_cover(
                img_src_2,
                img_dst_2,
                limit_size=eval(limit_size_2),
                limit_width=eval(limit_width_2),
                limit_height=eval(limit_height_2),
                max_workers=eval(max_workers_2),
            )
            st.success("压缩完成！")
            with st.expander("压缩信息"):
                st.write(info)


if __name__ == "__main__":
    page_init("图片压缩WebP", "🍭")
    page_main_1()
    with st.expander("实现说明"):
        contents = ["根据指定宽度和大小将图片压缩为`webp`格式(基于`cwebp`)"]
        page_md(contents)

    st.markdown("---")

    page_main_2()
    with st.expander("实现说明"):
        contents = ["1. 根据指定的宽高裁剪图片", "2. 压缩到限定大小(基于`cwebp`)"]
        page_md(contents)
