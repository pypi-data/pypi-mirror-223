"""
Created on 2016/12/5
@author: lijc210@163.com
Desc: 功能描述。
"""

import logging

from kazoo.client import KazooClient

logging.basicConfig()

zk = KazooClient(
    hosts="node11:2181,node12:2181,node13:2181,node14:2181,node15:2181,node16:2181,node17:2181"
)
zk.start()
print(zk.exists("zkkafkaspout1"))
print(zk.exists("consumers"))

print(zk.get_children("/consumers"))

data, stat = zk.get("/consumers")
print("Version: {}, data: {}".format(stat.version, data.decode("utf-8")))

zk.stop()
