"""
=========================================================================
@File Name: 4_👺_Auto-MkDocs.py
@Time: 2024/8/6 下午7:39
@Program IDE：PyCharm
@Create by Author: 一一风和橘
@Motto: "The trick, William Potter, is not minding that it hurts."
@Description:
- 
- 
=========================================================================
"""
import os
import random

import streamlit as st
from config import INIT

from koko_learn.MkDocTools import AutoMkdocs


def page_init():
    st.set_page_config(
        page_title="Auto-MkDocs",
        page_icon="👺",
        layout="wide",
        initial_sidebar_state="auto",
        menu_items={
            # 'Get Help': 'https://www.extremelycoolapp.com/help',
            # 'Report a bug': "https://www.extremelycoolapp.com/bug",
            'About': f"### 👺Auto-MkDocs \n\n {INIT.AUTHOR}"
        }
    )
    st.title('👺Auto-MkDocs')
    st.caption(INIT.AUTHOR)

def compress_rename(img_src,limit_width,max_workers):
    am = AutoMkdocs(path_src=img_src,
                    limit_size=50,
                    limit_width=int(limit_width),
                    max_workers=int(max_workers)
                    )
    am.run(is_auto=False)
    files = os.listdir(am.path_src)
    for file in files:
        os.rename(f'{am.path_dst}/{file.split(".")[0]}.webp',
                  f'{am.path_dst}/low-{file.split(".")[0]}.webp')


def page_main():
    col1, col3, col2 = st.columns((4.5, 1, 4.5))
    with col2:
        st.markdown('### 实现说明')
        st.markdown('1. 为图片添加水印')
        st.markdown('2. 压缩到限定宽度和大小(基于`pillow`)')
    with col1:
        col11, col12, col13, col4 = st.columns(4)
        with col11:
            limit_size = st.text_input('限制大小/kb',
                                       key='limit_size',
                                       value='500'
                                       )
        with col12:
            limit_width = st.text_input('限制宽度/px',
                                        key='limit_width',
                                        value='2560'
                                        )
        with col13:
            max_workers = st.selectbox("工作核心数",
                                       (str(INIT.MAX_WORKERS), str(INIT.MAX_WORKERS // 2), str(INIT.MAX_WORKERS // 4)),
                                       index=0,
                                       key='max_workers'
                                       )

        with col4:
            if_compress = st.radio('重新压缩WebP',
                                   ['True', 'False'],
                                   index=0,
                                   key='if_compress'
                                   )
            if_compress = bool(1 if if_compress == 'True' else 0)

        img_src = st.text_input('源路径',
                                key='img_src'
                                )

        if st.button('生成水印', key='img_btn'):
            if img_src:
                img_src = os.path.abspath(img_src)
                if 'am' not in st.session_state:
                    st.session_state.am = AutoMkdocs(path_src=img_src,
                                                     limit_size=int(limit_size),
                                                     limit_width=int(limit_width),
                                                     max_workers=int(max_workers)
                                                     )
                if if_compress:
                    compress_rename(img_src,limit_width,max_workers)
                    st.session_state.am.run(is_auto=False)

                    st.success('👺 自动化流程结束！')
                    with st.expander("压缩信息"):
                        info = st.session_state.am.compress_res
                        st.write(info)
        st.markdown('---')
        if 'am' in st.session_state:
            dst = st.session_state.am.path_dst
            title = st.session_state.am.title
            files = os.listdir(f'{dst}/{title}')
            random.shuffle(files)

            if 'wall_1' not in st.session_state:
                st.session_state.wall_1 = ''
            if 'wall_2' not in st.session_state:
                st.session_state.wall_2 = '\n'.join(files)

            st.session_state.wall_1 = st.text_area(label='wall-1排序',
                                                   value=st.session_state.wall_1,
                                                   key='wall-1'
                                                   )
            st.session_state.wall_2 = st.text_area(label='wall-2排序',
                                                   value=st.session_state.wall_2,
                                                   key='wall-2',
                                                   height=480
                                                   )
            if st.button('预览'):
                wall_1 = [item for item in st.session_state.wall_1.split('\n') if item != '']
                wall_2 = [item for item in st.session_state.wall_2.split('\n') if item != '']
                with col2:
                    for line in wall_1:
                        tmp = line.strip()
                        if tmp == '':
                            continue
                        pth = f'{dst}/{title}/{tmp}'
                        st.image(pth, caption=tmp)
                    cols = {}
                    for i in range(len(wall_2)):
                        cols[i] = st.columns(2)
                    for i, line in enumerate(wall_2):
                        tmp = line.strip()
                        if tmp == '':
                            continue
                        pth = f'{dst}/{title}/{tmp}'
                        with cols[i // 2][i % 2]:
                            st.image(pth, caption=tmp)

            if st.button('生成md'):
                wall_1 = [item for item in st.session_state.wall_1.split('\n') if item != '']
                wall_2 = [item for item in st.session_state.wall_2.split('\n') if item != '']
                res = st.session_state.am.generate_md(wall_1,
                                                      wall_2)
                if not res:
                    st.success('👺 md文件生成结束!')


if __name__ == '__main__':
    page_init()
    page_main()
