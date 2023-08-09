"""
@Time   : 2019-06-06
@author : lijc210@163.com
@Desc:  : 功能描述。
"""
import traceback
from multiprocessing import Pool

import wget


def download(url, out="img"):
    try:
        file_name = wget.download(url, out)
    except Exception:
        traceback.print_exc()
        file_name = ""
    return file_name


def batch_download(url_list):
    pool = Pool(30)
    res = pool.starmap(download, url_list)
    pool.close()
    pool.join()
    f1 = open("error.txt", "w")
    f2 = open("right.txt", "w")
    for img_path in res:
        if img_path:
            f2.write(img_path + "\n")
        else:
            f1.write(img_path + "\n")


if __name__ == "__main__":
    # file_name = download("https://www.baidu.com/img/dong_ea2fa2b4265f8de36695726995008ec0.gif","img")
    url_list = [
        ("https://www.baidu.com/img/dong_ea2fa2b4265f8de36695726995008ec0.gif", "img"),
        (
            "httpss://gss0.bdstatic.com/5bVWsj_p_tVS5dKfpU_Y_D3/res/r/image/2017-09-26/352f1d243122cf52462a2e6cdcb5ed6d.png",
            "img",
        ),
    ]
    batch_download(url_list)
