"""
Created on 2016/6/12
@author: lijc210@163.com
Desc: 功能描述。

auto_offset_reset参数:
earliest
当各分区下有已提交的offset时，从提交的offset开始消费；无提交的offset时，从头开始消费
latest
当各分区下有已提交的offset时，从提交的offset开始消费；无提交的offset时，消费新产生的该分区下的数据
none
topic各分区都存在已提交的offset时，从offset后开始消费；只要有一个分区不存在已提交的offset，则抛出异常

auto_commit_enable参数
在kafka拉取到数据之后就直接提交offset
设置为Flase的时候不需要添加 consumer_group

reset_offset_on_start参数：
为false，那么消费会从上一次消费的偏移量之后开始进行（比如上一次的消费偏移量为4，那么消费会从5开始）
为true，会自动从 auto_offset_reset 指定的位置开始消费


目前是配置为：上一次的消费偏移量开始读
"""

from pykafka import KafkaClient
from pykafka.simpleconsumer import OffsetType


class PykafkaClient:
    def __init__(
        self,
        hosts="node16:9092,node17:9092",
        topic="note_new",
        zookeeper_connect="node11:2181,node12:2181,node13:2181,node14:2181,node15:2181,node16:2181,node17:2181",
        auto_offset_reset=OffsetType.EARLIEST,
        reset_offset_on_start=False,
        offset=None,
    ):
        self.hosts = hosts
        self.topic = topic
        self.zookeeper_connect = zookeeper_connect
        self.auto_offset_reset = auto_offset_reset
        self.reset_offset_on_start = reset_offset_on_start
        self.offset = offset

    def conn(self):
        client = KafkaClient(hosts=self.hosts)
        # print client.topics
        topic = client.topics[self.topic]
        partitions = topic.partitions
        print("查看所有分区 {}".format(partitions))
        earliest_offset = topic.earliest_available_offsets()
        print("获取最早可用的offset {}".format(earliest_offset))
        last_offset = topic.latest_available_offsets()
        print("最近可用offset {}".format(last_offset))

        balanced_consumer = topic.get_balanced_consumer(
            consumer_group=self.topic,
            auto_commit_enable=False,
            auto_offset_reset=self.auto_offset_reset,
            reset_offset_on_start=self.reset_offset_on_start,
            zookeeper_connect=self.zookeeper_connect,
        )
        if self.offset is not None:  # 从指定offset读取
            offz = [(partitions[k], self.offset) for k in partitions]
            balanced_consumer.reset_offsets(offz)
        return balanced_consumer

    def consumer(self):
        balanced_consumer = self.conn()
        for message in balanced_consumer:
            if message is not None:
                print(message.offset, message.value)
                # balanced_consumer.commit_offsets()  # 手动提交
            break


if __name__ == "__main__":
    # reset_offset_on_start=True时，从最开始读；否则从上一次的消费偏移量
    pykafka_client = PykafkaClient(auto_offset_reset=OffsetType.EARLIEST)
    # reset_offset_on_start=True时，从最开始读；否则从上一次的消费偏移量
    # pykafka_client = PykafkaClient()
    # 从指定offset读
    # pykafka_client = PykafkaClient(offset=100)
    pykafka_client.consumer()
