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
        hosts="10.207.38.169:9092",
        topic="note_new",
        zookeeper_connect="10.207.38.169:2181",
        auto_offset_reset=OffsetType.EARLIEST,
        reset_offset_on_start=False,
        offset=None,
        online=False,
        consumer_group=None,
    ):
        self.hosts = hosts
        self.topic = topic
        self.zookeeper_connect = zookeeper_connect
        self.auto_offset_reset = auto_offset_reset
        self.reset_offset_on_start = reset_offset_on_start
        self.offset = offset
        self.consumer_group = self.topic if online else self.topic + "_test"
        self.consumer_group = consumer_group if consumer_group else self.consumer_group
        self.client = KafkaClient(hosts=self.hosts)

    def conn(self):
        topic = self.client.topics[self.topic]
        partitions = topic.partitions
        print("查看所有分区 {}".format(partitions))
        earliest_offset = topic.earliest_available_offsets()
        print("获取最早可用的offset {}".format(earliest_offset))
        last_offset = topic.latest_available_offsets()
        print("最近可用offset {}".format(last_offset))

        earliest_offset_int, last_offset_int = 0, 0
        for _k, v in earliest_offset.items():
            earliest_offset_int = v.offset[0] - 1
            break
        for _k, v in last_offset.items():
            last_offset_int = v.offset[0] - 1
            break
        balanced_consumer = topic.get_balanced_consumer(
            consumer_group=self.consumer_group,
            auto_commit_enable=False,
            auto_offset_reset=self.auto_offset_reset,
            reset_offset_on_start=self.reset_offset_on_start,
            zookeeper_connect=self.zookeeper_connect,
        )
        if self.offset is not None:  # 从指定offset读取
            offz = [(partitions[k], self.offset) for k in partitions]
            balanced_consumer.reset_offsets(offz)
        return balanced_consumer, earliest_offset_int, last_offset_int

    def get_topics(self):
        # print client.topics
        return self.client.topics

    def get_last_offset(self):
        topic = self.client.topics[self.topic]
        return topic.latest_available_offsets()

    def consumer(self):
        balanced_consumer, earliest_offset_int, last_offset_int = self.conn()
        for message in balanced_consumer:
            if message is not None:
                print(message.offset, message.value)
                # balanced_consumer.commit_offsets()  # 手动提交
            break

    def consumer2(self):
        balanced_consumer, earliest_offset_int, last_offset_int = self.conn()
        for message in balanced_consumer:
            if message is not None:
                print(message.offset, message.value)
                balanced_consumer.commit_offsets()  # 手动提交
                print(message.offset, last_offset_int)
                if message.offset >= last_offset_int - 1:
                    print("break")
                    break

    def reset_offset(self):
        balanced_consumer, earliest_offset_int, last_offset_int = self.conn()
        # 手动提交offset
        balanced_consumer.commit_offsets()
        print(balanced_consumer, earliest_offset_int, last_offset_int)


if __name__ == "__main__":
    # reset_offset_on_start=True时，从最开始读；否则从上一次的消费偏移量
    # pykafka_client = PykafkaClient(auto_offset_reset=OffsetType.EARLIEST)
    # reset_offset_on_start=True时，从最新开始读；否则从上一次的消费偏移量
    # pykafka_client = PykafkaClient(auto_offset_reset=OffsetType.LATEST)
    # 从指定offset读
    pykafka_client = PykafkaClient(offset=100)
    # pykafka_client = PykafkaClient(topic="note_new", offset=1112944)
    # pykafka_client.consumer()
    # pykafka_client.consumer2()
    # pykafka_client.reset_offset()
    pykafka_client.get_topics()
