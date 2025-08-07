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

import streamlit as st

from koko_film.koko_marker import KokoWaterMark
from koko_film.utils.page_init import page_init, page_md


def page_main():
    options = ["MARK_0", "MARK_1", "MARK_2", "MARK_3", "MARK_4", "MARK_5", "MARK_CONAN"]
    select_style = st.segmented_control(
        "水印样式",
        options,
        selection_mode="multi",
        default=[
            "MARK_0",
            "MARK_1",
            "MARK_2",
            "MARK_3",
            "MARK_4",
            "MARK_5",
            "MARK_CONAN",
        ],
    )
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

    col1, col2, _ = st.columns(3)
    with col1:
        img_src = st.text_input(
            "图片路径",
            key="img_src",
        )

    if st.button("生成水印", key="img_btn") and img_src:
        with st.spinner("等待进程...", show_time=True):
            wm = KokoWaterMark(
                path_root=img_src,
                select_style=select_style,
                aim_width=int(limit_width),
                aim_size=int(limit_size),
            )
            wm.run()
            info = wm.webp_report()
            st.success("添加水印完成！")
            with st.expander("压缩信息"):
                st.write(info)


def page_ref():
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.image("./common/sources/images/DSCF9285.webp", caption="样式 0")
    with col2:
        st.image("./common/sources/images/DSCF9304.webp", caption="样式 1")
    with col3:
        st.image("./common/sources/images/DSCF9302.webp", caption="样式 2")
    with col4:
        st.image("./common/sources/images/DSCF9307.webp", caption="样式 3")


if __name__ == "__main__":
    page_init("图片水印", "🍿")
    page_main()

    page_ref()

    contents = [
        "### 实现说明",
        "1. 为图片添加水印",
        "2. 压缩到限定宽度和大小(基于`pillow`)",
    ]
    page_md(contents)
