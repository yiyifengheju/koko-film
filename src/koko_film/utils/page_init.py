"""
=========================================================================
@File Name: page_init.py
@Time: 2025/3/19 23:48
@Program IDE: PyCharm
@Create by Author: 一一风和橘
@Motto: "The trick, William Potter, is not minding that it hurts."
@Description:
-
-
=========================================================================
"""

import streamlit as st

try:
    from ..config import CONFIG
except ImportError:
    from config import CONFIG


def page_init(title, icon):
    st.set_page_config(
        page_title=title,
        page_icon=icon,
        layout="wide",
        initial_sidebar_state="auto",
        menu_items={
            # 'Get Help': 'https://www.extremelycoolapp.com/help',
            # 'Report a bug': "https://www.extremelycoolapp.com/bug",
            "About": f"### {icon}{title} \n\n {CONFIG.AUTHOR}",
        },
    )
    st.title(f"{icon} {title}")
    st.caption(f"🐸 {CONFIG.AUTHOR}&ensp;&ensp;🍐 {CONFIG.VERSION}")


def page_md(contents):
    for item in contents:
        st.markdown(item, unsafe_allow_html=True)
