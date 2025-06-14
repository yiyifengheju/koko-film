"""
=========================================================================
@File Name: 3_🍿_图片水印.py
@Time: 2024/5/31 上午1:19
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

try:
    from ..config import CONFIG
    from ..pic_tools import KokoWaterMark
    from ..utils.page_init import page_init, page_md


except ImportError:
    from config import CONFIG
    from pic_tools import KokoWaterMark
    from utils.page_init import page_init, page_md


def page_main():
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        limit_size = st.text_input(
            "限制大小/kb",
            key="limit_size",
            value="500",
        )
    st.markdown("")
    with col2:
        limit_width = st.text_input(
            "限制宽度/px",
            key="limit_width",
            value="2560",
        )
    with col3:
        style_idx = st.selectbox(
            "水印样式",
            ("MARK_0", "MARK_1", "MARK_2", "MARK_3", "MARK_4"),
            index=1,
            key="style_idx",
        )
    with col4:
        cam_make = st.selectbox(
            "相机品牌",
            ("FujiFilm", "SONY"),
            index=0,
            key="cam_make",
        )
    with col5:
        max_workers = st.selectbox(
            "工作核心数",
            (str(CONFIG.MAX_WORKERS), str(CONFIG.MAX_WORKERS // 2), str(CONFIG.MAX_WORKERS // 4)),
            index=0,
            key="max_workers",
        )
    col1, col2 = st.columns(2)
    with col1:
        img_src = st.text_input(
            "图片路径",
            key="img_src",
        )

    if st.button("生成水印", key="img_btn") and img_src:
        tmp = Path(img_src, os.pardir).absolute()
        folder_name = img_src.split("/")[-1]
        img_dst = f"{tmp}/{folder_name}_MARKER"
        if not Path(img_dst).exists():
            Path(img_dst).mkdir(parents=True, exist_ok=True)

        with st.spinner("等待进程..."):
            wm = KokoWaterMark(
                path_src=img_src,
                path_dst=img_dst,
                aim_size=eval(limit_size),
                aim_width=eval(limit_width),
                watermark_style=eval(style_idx),
                camera_make=cam_make,
                init_info=None,
                max_workers=eval(max_workers),
            )
            # info = wm.run()
            wm.run()
            info = ""
            st.success("压缩完成！")
            with st.expander("压缩信息"):
                st.write(info)

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.image("./images/DSCF9285.webp", caption="样式 0")
    with col2:
        st.image("./images/DSCF9304.webp", caption="样式 1")
    with col3:
        st.image("./images/DSCF9302.webp", caption="样式 2")
    with col4:
        st.image("./images/DSCF9307.webp", caption="样式 3")


if __name__ == "__main__":
    page_init("图片水印", "🍿")
    page_main()

    contents = [
        "### 实现说明",
        "1. 为图片添加水印",
        "2. 压缩到限定宽度和大小(基于`pillow`)",
    ]
    page_md(contents)
