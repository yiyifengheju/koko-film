"""
=========================================================================
@File Name: 9_🔧_系统设置.py
@Time: 2024/5/30 上午12:54
@Program IDE：PyCharm
@Create by Author: 一一风和橘
@Motto: "The trick, William Potter, is not minding that it hurts."
@Description:
-
- 🍿
=========================================================================
"""

import shutil
from pathlib import Path

import streamlit as st
import toml

try:
    from ..config import CONFIG
except ImportError:
    from config import CONFIG


def page_init():
    st.set_page_config(
        page_title="系统设置",
        page_icon="🔧",
        layout="wide",
        initial_sidebar_state="auto",
        menu_items={
            # 'Get Help': 'https://www.extremelycoolapp.com/help',
            # 'Report a bug': "https://www.extremelycoolapp.com/bug",
            "About": f"🔧系统设置 \n\n {CONFIG.AUTHOR}",
        },
    )
    st.title("🔧系统设置")
    st.caption(CONFIG.AUTHOR)


def page_main():
    col1, col2, col3 = st.columns(3)
    with col1:
        conf_theme = st.selectbox(
            "显示模式",
            ("DARK", "LIGHT"),
            key="conf_theme",
        )
        st.write("")

    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        if st.button("保存配置", key="btn_save_conf"):
            match CONFIG.SYSTEM:
                case "Windows":
                    conf_dict = {
                        "THEME": conf_theme,
                    }
                case "Linux":
                    conf_dict = {
                        "THEME": conf_theme,
                    }
                case _:
                    assert 0

            with Path("./config.toml").open("w", encoding="utf-8") as f:
                toml.dump(conf_dict, f)

            streamlit_config = toml.load("./.streamlit/config.toml")
            streamlit_config["theme"]["base"] = conf_theme.lower()
            with Path("./.streamlit/config.toml").open("w", encoding="utf-8") as f:
                toml.dump(streamlit_config, f)
            st.rerun()

    with col2:
        if st.button("恢复默认", key="btn_default_conf"):
            shutil.copy("./default.toml", "./config.toml")
            st.rerun()


if __name__ == "__main__":
    # 页面配置
    page_init()
    # 页面功能
    page_main()
