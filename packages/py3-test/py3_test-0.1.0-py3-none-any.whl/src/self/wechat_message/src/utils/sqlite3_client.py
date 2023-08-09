"""
@Time   : 2018/8/3
@author : lijc210@163.com
@Desc:  : 功能描述。
"""
import sqlite3
import time


class Sqlite3Client:
    def __init__(self, db=None, cursorclass=None):
        self.db = db
        self.cursorclass = cursorclass

    @staticmethod
    def dict_factory(cursor, row):
        d = {}
        for idx, col in enumerate(cursor.description):
            d[col[0]] = row[idx]
        return d

    def conn(self):
        conn = sqlite3.connect(self.db)
        if self.cursorclass == "dict":
            conn.row_factory = self.dict_factory
        cursor = conn.cursor()
        return conn, cursor

    def query(self, sql):
        """
        SELECT *  from COMPANY

        :param sql:
        :return:
        """
        conn, cursor = self.conn()
        cursor.execute(sql)
        results = cursor.fetchall()
        cursor.close()
        conn.close()
        return results

    def insert(self, sql, lock_sleep=0):
        """
        INSERT INTO COMPANY (ID,NAME,AGE,ADDRESS,SALARY) \
        VALUES (1, 'Paul', 32, 'California', 20000.00 )

        更新插入：
        REPLACE INTO COMPANY (ID,NAME,AGE,ADDRESS,SALARY) \
        VALUES (1, 'Paul', 32, 'California', 20000.00 )

        :param sql:
        :return:
        """
        conn, cursor = self.conn()
        if lock_sleep:
            try:
                cursor.execute(sql)
            except sqlite3.OperationalError:
                print("database locked")
                time.sleep(lock_sleep)
                cursor.execute(sql)
        else:
            cursor.execute(sql)
        conn.commit()
        cursor.close()
        conn.close()
        return cursor.lastrowid

    def insertmany(self, sql, sqlDataList):
        """

        :param sql: INSERT INTO COMPANY (ID,NAME,AGE,ADDRESS,SALARY) VALUES (?, ?, ?, ?, ?)
        :param sqlDataList: [[1, 'Paul', 32, 'California', 20000.00],[2, 'Paul', 32, 'California', 20000.00]]
        :return:
        """

        conn, cursor = self.conn()
        cursor.executemany(sql, sqlDataList)
        lastrowid = cursor.lastrowid
        conn.commit()
        cursor.close()
        conn.close()
        return lastrowid

    def execute(self, sql):
        """

        删除表：
        drop table COMPANY

        创建表：
        CREATE TABLE IF NOT EXISTS COMPANY
           (ID INTEGER PRIMARY KEY    autoincrement,
           NAME           TEXT    NOT NULL,
           AGE            INT     NOT NULL,
           ADDRESS        CHAR(50),
           SALARY         REAL)

        :param sql:
        :return:
        """
        conn, cursor = self.conn()
        cursor.execute(sql)
        conn.commit()
        cursor.close()
        conn.close()


if __name__ == "__main__":
    sqlite3_client = Sqlite3Client("tests.db")
    sql = """
            CREATE TABLE IF NOT EXISTS COMPANY
           (ID INTEGER PRIMARY KEY    autoincrement,
           NAME           TEXT    NOT NULL,
           AGE            INT     NOT NULL,
           ADDRESS        CHAR(50),
           SALARY         REAL)
    """
    sqlite3_client.execute(sql)

    sql = "        INSERT INTO COMPANY (NAME,AGE,ADDRESS,SALARY) \
        VALUES ('Paul', 32, 'California', 20000.00 )"

    print(sqlite3_client.insert(sql))

    sql = "SELECT *  from COMPANY"
    print(sqlite3_client.query(sql))
