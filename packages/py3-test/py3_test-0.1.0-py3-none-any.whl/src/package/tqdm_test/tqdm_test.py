"""
@Time   : 2019/3/7
@author : lijc210@163.com
@Desc:  : 功能描述。
"""
import time

from tqdm import trange

# for i in tqdm(range(100)):
#     time.sleep(0.1)

for _i in trange(100):
    time.sleep(0.1)

# pbar = tqdm(["a", "b", "c", "d"])
# for char in pbar:
#     pbar.set_description("Processing %s" % char)
