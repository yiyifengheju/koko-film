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

import streamlit as st

try:
    from ..pic_tools import raf_renamer
    from ..utils.page_init import page_init, page_md

except ImportError:
    from pic_tools import raf_renamer
    from utils.page_init import page_init, page_md


def page_main():
    cols = st.columns([6, 4])
    with cols[0]:
        raf_src = st.text_input(
            "RAF源路径",
            key="raf_src",
        )

        raf_dst = st.text_input(
            "RAF目标路径",
            value=r"H:\RAF_TMP",
            key="raf_dst",
        )
        aim_model = st.selectbox(
            "目标相机Model",
            options=["", "X-T50", "X100VI", "X-T5", "X-H2", "X-H2s", "X-S20", "X-T30II", "X-E4"],
            index=0,
        )

        col11, col12, _, _ = st.columns(4)
        with col11:
            if st.button("重命名RAF", key="raf_btn") and raf_src and raf_dst:
                with st.spinner("等待进程..."):
                    raf_renamer(raf_src, raf_dst, aim_model)
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
    page_main()
