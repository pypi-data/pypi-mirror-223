"""
@Time   : 2019/4/23
@author : lijc210@163.com
@Desc:  : 功能描述。
"""
import queue
import telnetlib
import threading


def get_ip_status(ip):
    server = telnetlib.Telnet()
    for port in range(20, 100):
        try:
            server.open(ip, port)
            print("{} port {} is open".format(ip, port))
        except Exception:
            print("{} port {} is not open".format(ip, port))
        finally:
            server.close()


def check_open(q):
    try:
        while True:
            ip = q.get_nowait()
            get_ip_status(ip)
    except queue.Empty:
        pass


if __name__ == "__main__":
    host = ["10.10.20.165"]  # 这里模拟多IP地址的情况，也可以从文件中读取IP——list
    q = queue.Queue()
    for ip in host:
        q.put(ip)
    threads = []
    for _i in range(100):
        t = threading.Thread(target=check_open, args=(q,))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()
