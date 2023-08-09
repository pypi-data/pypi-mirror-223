"""
Created on 2016/9/21
@author: lijc210@163.com
Desc: 功能描述。
"""
from fabric import Connection, SerialGroup

host_list = "node11"
host_list = (
    "node11",
    "node12",
    "node13",
    "node14",
    "node15",
    "node16",
    "node17",
    "node18",
    "node21",
    "node22",
    "node23",
    "hadoop24",
    "hadoop25",
    "hadoop26",
    "hadoop27",
)
host_list = (
    "node12",
    "node13",
    "node14",
    "node15",
    "node16",
    "node17",
    "node18",
    "node21",
    "node22",
    "node23",
    "hadoop24",
    "hadoop25",
    "hadoop26",
    "hadoop27",
)
# result = SerialGroup(*host_list).run('hostname')

for host in host_list:
    result = Connection(host).put(
        "/home/hadoop/Miniconda3-latest-Linux-x86_64.sh",
        remote="/home/hadoop/Miniconda3-latest-Linux-x86_64.sh",
    )
    print("{}: {}".format(host, result.remote))

result = SerialGroup(*host_list).run("/home/hadoop/miniconda3/bin/pip install retry")
