"""
Created on 2017/11/22 0022 17:31
@author: lijc210@163.com
Desc: 远程查询hive
"""
import traceback
from platform import python_version

from pyhive import hive
from retry import retry

if python_version().startswith("2"):
    pass


class HiveClient:
    def __init__(self, host=None, port=10000, username=None):
        self.host = host
        self.port = port
        self.username = username

    def Conn(self):
        conn = hive.Connection(host=self.host, port=self.port, username=self.username)
        cursor = conn.cursor()
        return conn, cursor

    def query(self, sql):
        conn, cursor = self.Conn()
        try:
            cursor.execute(sql)
        except Exception:
            conn, cursor = self.Conn()
            traceback.print_exc()
        results = cursor.fetchall()
        cursor.close()
        conn.close()
        return results

    def execute(self, sql):
        conn, cursor = self.Conn()
        results = cursor.execute(sql)
        print(results)

    @retry(tries=3, delay=2)  # 报错重试
    def execute_with_retry(self, sql):
        conn, cursor = self.Conn()
        results = cursor.execute(sql)
        print(results)


if __name__ == "__main__":
    hive_client = HiveClient(host="10.10.23.11", port=10000, username="hadoop")
    sql = "select zx_need_id,user_unique , zx_message   from dw.kn1_zx_need  where month_num>='201801' limit 10"
    print(hive_client.query(sql))
