"""
Created on 2016/5/10
@author: lijc210@163.com
Desc: 功能描述。

pip install redis-py-cluster

"""
from rediscluster import StrictRedisCluster

startup_nodes = [
    {"host": "10.10.20.97", "port": "7000"},
    {"host": "10.10.20.97", "port": "7001"},
]
conn = StrictRedisCluster(startup_nodes=startup_nodes, decode_responses=True)  # 连接集群
print(conn.cluster_nodes())
print(conn.cluster_info())

if __name__ == "__main__":
    pass
