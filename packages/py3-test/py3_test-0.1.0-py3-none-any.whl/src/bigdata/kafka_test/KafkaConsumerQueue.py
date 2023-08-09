"""
Created on 2016/6/12
@author: lijc210@163.com
Desc: 功能描述。
"""

from queue import Queue
from threading import Thread

from kafka import KafkaConsumer

# To consume latest messages and auto-commit offsets
consumer = KafkaConsumer(
    "note_new",
    # group_id='my-group',
    bootstrap_servers=["node16:9092"],
)
# for message in consumer:
#     # message value and key are raw bytes -- decode if necessary!
#     # e.g., for unicode: `message.value.decode('utf-8')`
#     print ("%s:%d:%d: key=%s value=%s" % (message.topic, message.partition,
#                                           message.offset, message.key,
#                                           message.value))


class ProducerThread(Thread):
    def __init__(self, queue):
        Thread.__init__(self)
        self.queue = queue

    def run(self):
        for message in consumer:
            self.queue.put(message.value)


class ConsumerThread(Thread):
    def __init__(self, queue):
        Thread.__init__(self)
        self.queue = queue

    def run(self):
        while True:
            print(self.queue.get())
            self.queue.task_done()


queue = Queue()
ProducerThread(queue).start()
# ConsumerThread(queue).start()
for _x in range(10):
    ConsumerThread(queue).start()
