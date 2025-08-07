"""
=========================================================================
@File Name: webp2md.py
@Time: 2025/7/28 22:45
@Program IDE: PyCharm
@Create by Author: 一一风和橘
@Motto: "The trick, William Potter, is not minding that it hurts."
@Description:
-
-
=========================================================================
"""

import shutil
from pathlib import Path

image_base = Path(r"H:\600_PycharmProjects\opus_mkdocs\src\opus_gallery\docs\images")
blog_base = Path(r"H:\600_PycharmProjects\opus_mkdocs\src\opus_gallery\docs\blog")


def main():
    path_img = Path(r"C:\Users\mastermao\Desktop\tmp\WEBP")
    mds = []
    for img in path_img.iterdir():
        date = img.name.split("_")[0]
        path_dst = Path(image_base, date)
        path_dst.mkdir(parents=True, exist_ok=True)
        shutil.copy(img, Path(path_dst, img.name))
        tmp = f"![{img.name}](/images/{date}/{img.name})\n\n"
        mds.append(tmp)
    with Path(blog_base, "tmp.md").open(mode="w") as f:
        f.writelines(mds)


if __name__ == "__main__":
    main()
