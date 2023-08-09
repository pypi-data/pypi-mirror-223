import pymysql
from pymysql.cursors import DictCursor


class MySqlClient:
    def __init__(self, conn_dict, charset="utf8", cursorclass="dict"):
        self.host = conn_dict["host"]
        self.user = conn_dict["user"]
        self.passwd = conn_dict["passwd"]
        self.db = conn_dict["db"]
        self.charset = charset
        self.port = conn_dict["port"]
        self.cursorclass = cursorclass
        self.conn, self.cursor = self.connection()

    def check_connection(self):
        # print self.conn.ping(reconnect=True)
        # if self.conn.open is False:
        #     self.conn, self.cursor = self.connection()
        try:
            self.conn.ping(reconnect=True)
        except Exception:
            self.conn, self.cursor = self.connection()

    def connection(self):
        if self.cursorclass == "dict":
            conn = pymysql.connect(
                host=self.host,
                user=self.user,
                passwd=self.passwd,
                db=self.db,
                charset=self.charset,
                port=self.port,
                cursorclass=DictCursor,
                autocommit=True,
            )
        elif self.cursorclass == "ss_dict":
            conn = pymysql.connect(
                host=self.host,
                user=self.user,
                passwd=self.passwd,
                db=self.db,
                charset=self.charset,
                port=self.port,
                cursorclass=pymysql.cursors.SSDictCursor,
                autocommit=True,
            )
        elif self.cursorclass == "ss_list":
            conn = pymysql.connect(
                host=self.host,
                user=self.user,
                passwd=self.passwd,
                db=self.db,
                charset=self.charset,
                port=self.port,
                cursorclass=pymysql.cursors.SSCursor,
                autocommit=True,
            )
        else:
            conn = pymysql.connect(
                host=self.host,
                user=self.user,
                passwd=self.passwd,
                db=self.db,
                charset=self.charset,
                port=self.port,
                autocommit=True,
            )
        cursor = conn.cursor()
        return conn, cursor

    def query(self, sql):
        self.check_connection()
        self.cursor.execute(sql)
        results = self.cursor.fetchall()
        self.conn.close()
        return results

    def query_cursor(self, sql):
        """
        游标查询，需要返回大数量时使用
        :param sql:
        :return:
        """
        self.check_connection()
        self.cursor.execute(sql)
        self.conn.close()
        return self.cursor

    def insert(self, sql):
        """
        INSERT INTO table_name ( field1, field2,...fieldN )
                       VALUES
                       ( value1, value2,...valueN );
        :param sql:
        :return:
        """
        self.check_connection()
        self.cursor.execute(sql)
        self.conn.commit()
        self.conn.close()

    def update(self, sql):
        self.check_connection()
        self.cursor.execute(sql)
        self.conn.commit()
        self.conn.close()

    def execute(self, sql):
        self.check_connection()
        self.cursor.execute(sql)
        self.conn.commit()
        self.conn.close()

    def executemany(self, sql, sqlDataList):
        # tests = [['a','b','c'],['d','f','e']]
        self.check_connection()
        self.cursor.executemany(sql, sqlDataList)
        lastrowid = self.cursor.lastrowid
        self.conn.commit()
        self.conn.close()
        return lastrowid

    # def __del__(self):
    #     self.cursor.close()
    #     self.conn.close()


if __name__ == "__main__":
    WORD_DB = {
        "host": "10.10.11.244",
        "user": "biuser",
        "passwd": "@biuser123",
        "db": "userdata",
        "port": 3309,
    }
    mysql_client = MySqlClient(conn_dict=WORD_DB)
    sql = "select * from userdata.dict_professionalterm limit 10"
    print(mysql_client.query(sql))
    # mysql_client = MySqlClient(conn_dict=WORD_DB, cursorclass="ss_dict")
    # sql = "select * from spider_data.question where source='太平洋'"
    # for x in mysql_client.query_cursor(sql):
    #     print(x)
