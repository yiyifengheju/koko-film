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

import streamlit as st
from config import INIT

from koko_learn.PicTools import compress_cover
from koko_learn.PicTools import compress_webp


def get_compress_info(path_src, path_dst, pre):
    import pandas as pd

    files = os.listdir(path_src)
    size_list = []
    for file in files:
        if os.path.isdir(os.path.join(path_src, file)):
            continue
        old_size = os.path.getsize(f'{path_src}/{file}')
        new_size = os.path.getsize(f'{path_dst}/{file.split(".")[0]}.webp')
        os.rename(f'{path_dst}/{file.split(".")[0]}.webp', f'{path_dst}/{pre}-{file.split(".")[0]}.webp')
        size_list.append([file, old_size, new_size, new_size / old_size])
    info = pd.DataFrame(size_list, columns=['FILE', 'MEM_OLD', 'MEM_NEW', 'RATE'])
    return info


def page_init():
    st.set_page_config(
        page_title="图片压缩WebP",
        page_icon="🍭",
        layout="wide",
        initial_sidebar_state="auto",
        menu_items={
            # 'Get Help': 'https://www.extremelycoolapp.com/help',
            # 'Report a bug': "https://www.extremelycoolapp.com/bug",
            'About': f"### 🍭图片压缩WebP \n\n {INIT.AUTHOR}"
        }
    )
    st.title('🍭 图片压缩')
    st.caption(INIT.AUTHOR)


def page_main_1():
    st.markdown('### 图片压缩')
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        limit_size = st.text_input('限制大小/kb',
                                   key='limit_size',
                                   value='500'
                                   )
    with col2:
        limit_width = st.text_input('限制宽度/px',
                                    key='limit_width',
                                    value='2560'
                                    )
    with col3:
        max_workers = st.selectbox("工作核心数",
                                   (str(INIT.MAX_WORKERS), str(INIT.MAX_WORKERS // 2), str(INIT.MAX_WORKERS // 4)),
                                   index=0,
                                   key='max_workers'
                                   )
    with col4:
        rename_pre = st.text_input('重命名',
                                   key='rename_pre',
                                   value=''
                                   )

    img_src = st.text_input('IMG_SRC',
                            key='img_src'
                            )

    if st.button('压缩Webp', key='img_btn'):
        if img_src:
            # tmp = os.path.abspath(os.path.join(img_src, os.pardir))
            tmp = os.path.abspath(img_src)
            img_dst = f'{tmp}/2_WEBP'
            if not os.path.exists(img_dst):
                os.mkdir(img_dst)

            with st.spinner('等待进程...'):
                compress_webp(img_src,
                              img_dst,
                              limit_size=eval(limit_size),
                              limit_width=eval(limit_width),
                              max_workers=eval(max_workers)
                              )
                st.success('压缩完成！')
            info = get_compress_info(img_src, img_dst, rename_pre)
            with st.expander("压缩信息"):
                st.write(info)
    st.markdown('### 实现说明')
    st.markdown('根据指定宽度和大小将图片压缩为`webp`格式(基于`cwebp`)')


def page_main_2():
    st.markdown('### 封面压缩')
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        limit_size_2 = st.text_input('限制大小/kb',
                                     key='limit_size_2',
                                     value='500'
                                     )
    with col2:
        limit_width_2 = st.text_input('限制宽度/px',
                                      key='limit_width_2',
                                      value='2560'
                                      )
    with col3:
        limit_height_2 = st.text_input('限制高度/px',
                                       key='limit_height_2',
                                       value='853'
                                       )
    with col4:
        max_workers_2 = st.selectbox("工作核心数",
                                     (str(INIT.MAX_WORKERS), str(INIT.MAX_WORKERS // 2), str(INIT.MAX_WORKERS // 4)),
                                     index=0,
                                     key='max_workers_2'
                                     )

    img_src_2 = st.text_input('IMG_SRC',
                              key='img_src_2'
                              )

    if st.button('压缩封面Webp', key='img_btn_2'):
        if img_src_2:
            tmp = os.path.abspath(os.path.join(img_src_2, os.pardir))
            img_dst_2 = f'{tmp}/3_COVER_WEBP'
            if not os.path.exists(img_dst_2):
                os.mkdir(img_dst_2)

            with st.spinner('等待进程...'):
                info = compress_cover(img_src_2,
                                      img_dst_2,
                                      limit_size=eval(limit_size_2),
                                      limit_width=eval(limit_width_2),
                                      limit_height=eval(limit_height_2),
                                      max_workers=eval(max_workers_2)
                                      )
                st.success('压缩完成！')
                with st.expander("压缩信息"):
                    st.write(info)
    st.markdown('### 实现说明')
    st.markdown('1. 根据指定的宽高裁剪图片')
    st.markdown('2. 压缩到限定大小(基于`cwebp`)')


if __name__ == '__main__':
    page_init()
    coll, colm, colr = st.columns([4.8, 0.4, 4.8])
    with coll:
        page_main_1()
    with colr:
        page_main_2()
