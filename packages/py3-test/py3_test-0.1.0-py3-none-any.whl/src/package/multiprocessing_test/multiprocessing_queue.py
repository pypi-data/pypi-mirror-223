"""
@Time   : 2019/5/30
@author : lijc210@163.com
@Desc:  : 功能描述。
"""
from multiprocessing import Queue

queue = Queue(maxsize=10)
print(queue.empty())
queue.put({"a": "b"})
print(queue.empty())

if __name__ == "__main__":
    print(queue.get())
    print("---main----")
