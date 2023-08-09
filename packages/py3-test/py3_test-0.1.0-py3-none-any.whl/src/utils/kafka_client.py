from pykafka import KafkaClient


# 使用python的pykafka编写kafka工具类
class KafkaTool:
    def __init__(
        self,
        hosts="",
        topic="",
        zookeeper_connect="",
        auto_offset_reset="",
        reset_offset_on_start="",
        offset="",
        online="",
        consumer_group="",
    ):
        self.hosts = hosts
        self.topic = topic
        self.zookeeper_connect = zookeeper_connect
        self.auto_offset_reset = auto_offset_reset
        self.reset_offset_on_start = reset_offset_on_start
        self.offset = offset
        self.consumer_group = consumer_group
        self.client = KafkaClient(hosts=self.hosts)
