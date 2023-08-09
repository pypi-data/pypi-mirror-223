"""
Created on 2016/5/10
@author: lijc210@163.com
Desc: 功能描述。
"""

# -*- coding:utf-8 -*-

import psycopg2


class PostgreSQL:
    def __init__(self):
        self.conn, self.cursor = self.Conn()

    def Conn(self):
        conn = psycopg2.connect(
            database="dw",
            user="postgres",
            password="postgres",
            host="10.10.23.100",
            port="5432",
        )
        cursor = conn.cursor()
        return conn, cursor

    # 查询
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

    def insert(self, sql):
        conn, cursor = self.Conn()
        try:
            self.cursor.execute(sql)
            self.conn.commit()
        except Exception as e:
            print(sql)
            print(e)
        cursor.close()
        conn.close()

    def insertmany(self, sql, sqlDataList):
        # print sql
        # test = [['0', '1', 'n', '', '3', 'aaa', '33.3333333333','aabb.aaa']]
        conn, cursor = self.Conn()
        try:
            self.cursor.executemany(sql, sqlDataList)
            # lastrowid = self.cursor.lastrowid
            self.conn.commit()
            # return lastrowid
        except Exception as e:
            print(sql)
            print(e)
        cursor.close()
        conn.close()


if __name__ == "__main__":
    pg = PostgreSQL()
    sql = """select ip_num,city from config.conf_ip_city_detail limit 10"""
    print(pg.query(sql))
