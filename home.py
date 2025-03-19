"""
=========================================================================
@File Name: home.py
@Time: 2024/5/13 上午2:39
@Program IDE：PyCharm
@Create by Author: 一一风和橘
@Motto: "The trick, William Potter, is not minding that it hurts."
@Description:
-
-
=========================================================================
"""

import sys

import streamlit as st
from utils.page_init import page_init

sys.path.append("..")


def page_main():
    st.markdown("### RAF工具")
    st.page_link("pages/1_🍅_RAF重命名.py", label="RAF重命名", icon="🍅")
    st.markdown("---")

    st.markdown("### WebP工具")
    st.page_link("pages/2_🍭_压缩Webp.py", label="压缩Webp", icon="🍭")
    st.page_link("pages/3_🍿_图片水印.py", label="图片水印", icon="🍿")
    st.markdown("---")

    st.markdown("### MkDocs工具")
    st.page_link("pages/4_👺_Auto-MkDocs.py", label="Auto-MkDocs", icon="👺")


if __name__ == "__main__":
    page_init("Aqua-Cam", "🦀")
    page_main()
