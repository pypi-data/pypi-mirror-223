"""
Created on 2016/8/5
@author: lijc210@163.com
Desc: 功能描述。
"""
from pyhive import presto


class PrestoClient:
    def __init__(self):
        pass

    def Conn(self):
        conn = presto.connect(host="10.10.23.11", port=8444, username="lijicong")
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

    def queryDict(self, sql):
        conn, cursor = self.Conn()
        try:
            cursor.execute(sql)
        except Exception as e:
            conn, cursor = self.Conn()
            print(e)
        results = cursor.fetchall()
        desc = []
        if cursor.description:
            desc = [field[0] for field in cursor.description]
        res_list = [dict(list(zip(desc, row, strict=True))) for row in results]
        cursor.close()
        conn.close()
        return res_list


if __name__ == "__main__":
    presto_client = PrestoClient()
    sql = """SELECT company_name,city_name from dw.ol_api_company_detail where city_name in (
select city_name from dw.ol_pub_city_new where business_type in ('直营落地','直营地级市')
)  GROUP BY company_name,city_name"""
    with open("zhiying.txt", "w", encoding="utf-8") as f:
        for company_name, city_name in presto_client.query(sql):
            f.write(company_name + "\t" + city_name + "\n")
