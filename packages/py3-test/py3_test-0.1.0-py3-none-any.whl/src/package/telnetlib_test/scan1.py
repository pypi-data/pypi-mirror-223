"""
@Time   : 2019/4/23
@author : lijc210@163.com
@Desc:  : 功能描述。
"""
import telnetlib
import threading


def get_ip_status(ip, port):
    server = telnetlib.Telnet()
    try:
        server.open(ip, port)
        print("{} port {} is open".format(ip, port))
    except Exception:
        print("{} port {} is not open".format(ip, port))
    finally:
        server.close()


if __name__ == "__main__":
    host = "10.10.20.165"
    threads = []
    for port in range(8000, 9000):
        t = threading.Thread(target=get_ip_status, args=(host, port))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()
