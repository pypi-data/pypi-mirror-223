"""
Created on 2017/11/22 0022 17:31
@author: lijc210@163.com
Desc:
"""

from pyhive import hive


class HiveClient:
    def __init__(self, host="10.10.23.11", port=10000, username="lijicong"):
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
        except Exception as e:
            conn, cursor = self.Conn()
            print(e)
        results = cursor.fetchall()
        cursor.close()
        conn.close()
        return results


if __name__ == "__main__":
    hive_client = HiveClient()
    sql = "select zx_need_id,user_unique , zx_message   from dw.kn1_zx_need  where month_num>='201801' limit 10"
    print(hive_client.query(sql))
