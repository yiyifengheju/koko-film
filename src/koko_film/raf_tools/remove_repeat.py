"""
=========================================================================
@File Name: remove_repeat.py
@Time: 2025/7/6 16:15
@Program IDE: PyCharm
@Create by Author: 一一风和橘
@Motto: "The trick, William Potter, is not minding that it hurts."
@Description:
-
-
=========================================================================
"""
import os
import hashlib

def get_file_hash(file_path):
    """计算文件的MD5哈希值"""
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def remove_duplicate_images(folder_path):
    """去除指定文件夹中的重复图片"""
    hash_dict = {}
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
                file_path = os.path.join(root, file)
                file_hash = get_file_hash(file_path)
                if file_hash in hash_dict:
                    print(f"发现重复图片: {file_path}")
                    # os.remove(file_path)  # 删除重复图片
                else:
                    hash_dict[file_hash] = file_path

# 使用示例
folder_path = 'path/to/your/image/folder'
remove_duplicate_images(folder_path)