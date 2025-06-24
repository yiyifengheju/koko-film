"""
=========================================================================
@File Name: test.py
@Time: 2025/6/19 21:59
@Program IDE: PyCharm
@Create by Author: 一一风和橘
@Motto: "The trick, William Potter, is not minding that it hurts."
@Description:
- 
- 
=========================================================================
"""
import os
from pathlib import Path

path_root = Path(r'H:\200_RAF')
for folder in path_root.iterdir():
    Path(folder, 'RAF').mkdir(parents=True, exist_ok=True)

