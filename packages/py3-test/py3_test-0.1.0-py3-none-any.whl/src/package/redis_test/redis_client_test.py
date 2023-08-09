"""
Created on 2016/5/10
@author: lijc210@163.com
Desc: 功能描述。

pip install redis-py-cluster

"""
import redis
from rediscluster import StrictRedisCluster


class RedisClient:
    def __init__(self, host=None, port=None, db=None, pool=False, startup_nodes=None):
        self.host = host
        self.port = port
        self.db = db
        self.pool = pool
        self.startup_nodes = startup_nodes
        self.client = self.conn()

    def conn(self):
        """
        连接
        集群模式只有一个db
        :return:
        """
        if self.startup_nodes:
            conn = StrictRedisCluster(
                startup_nodes=self.startup_nodes, decode_responses=True
            )  # 连接集群
        elif self.pool:
            pool = redis.ConnectionPool(
                host=self.host, port=self.port, db=self.db, decode_responses=True
            )
            conn = redis.Redis(connection_pool=pool)  # 连接池
        else:
            conn = redis.StrictRedis(
                host=self.host, port=self.port, db=self.db, decode_responses=True
            )
        return conn

    def _set(self):
        """
        设置字符串类型
        :return:
        """
        self.client.set("test", "test")
        print(self.client.get("test"))

    def _sadd(self):
        """
        设置无序集合类型
        :return:
        """
        self.client.sadd("test_set", *[1, 2, 3, 4])
        print(self.client.smembers("test_set"))

    def _zadd(self):
        """
        设置有序集合类型
        :return:
        """
        self.client.zadd("test_zset", **{"a": 1, "b": 10})
        print(self.client.zrangebyscore("test_zset", 0, 5))

    def _hmset(self):
        """
        设置哈希类型
        :return:
        """
        self.client.hmset("test_hash", {"a": 1, "b": 10})
        print(self.client.hgetall("test_hash"))


if __name__ == "__main__":
    # startup_nodes = [{"host": "10.10.20.97", "port": "7000"}, {"host": "10.10.20.97", "port": "7001"}]
    # rc = RedisClient(startup_nodes=startup_nodes).client
    # print (rc.get("test"))
    # # 验证redis服务是否正常
    # rc = RedisClient(startup_nodes=startup_nodes)
    # rc._set()
    # rc._sadd()
    # rc._zadd()
    # rc._hmset()

    r = RedisClient(host="10.10.20.165", port=6379, db=0).client
    print(r.smembers("unitSet"))
    print(r.smembers("unitSet1"))
