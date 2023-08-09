"""
@File    :   ck.py
@Time    :   2021/01/08 10:10:26
@Author  :   lijc210@163.com
@Desc    :   None
"""

import sqlalchemy as sa

engine = sa.create_engine("clickhouse://ck_readonly:shgqsh2020@114.116.224.81:8123/ads")

sql = "select * from ads_sales_shop_channel_etl limit 10"
conn = engine.connect()
res_obj = conn.execute(object_=sql)
print(dir(res_obj))
print(res_obj.keys())
print(res_obj._init_metadata())
