import logging
import multiprocessing
from multiprocessing import Pipe, Process

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s [*] %(processName)s %(message)s"
)


def send(pipe):
    message = ["spam"] + [42, "egg"]
    pipe.send(message)
    logging.info(f"A01 发送信息：{message}-------单向通信")
    pipe.close()


def talk(pipe):
    message = {"name": "Bob", "spam": 42}
    pipe.send(message)
    logging.info(f"B02 发送信息：{message}----双向通信")
    reply = pipe.recv()
    logging.info(f"B02 接收信息：{reply}-------双向通信")


def main(ctx):
    # 单向通信--------------------------------------------------------
    (A01, A02) = ctx.Pipe()
    sender = ctx.Process(target=send, args=(A01,))
    sender.start()
    logging.info(f"A02 接收信息：{A02.recv()}----------单向通信")  # 从send收到消息
    A02.close()

    # 双向通信---------------------------------------------------------
    (B01, B02) = Pipe()
    # 1.B02发送信息
    talking = Process(target=talk, args=(B02,))
    talking.start()
    logging.info(f"B01 接收信息：{B01.recv()}--双向通信")
    # 2.B01发送信息
    message = {x * 2 for x in "spam"}
    B01.send(message)
    logging.info(f"B01 发送信息{message}-------双向通信")

    talking.join()  # 阻塞并等待子进程通话完毕


if __name__ == "__main__":
    # windows 启动方式
    multiprocessing.set_start_method("spawn")
    # 获取上下文
    ctx = multiprocessing.get_context("spawn")
    main(ctx)
