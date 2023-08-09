"""
@author: lijc210@163.com
@file: kylinpy_client.py
@time: 2020/06/02
@desc: 功能描述。
"""

import sqlalchemy as sa

conn_str = "kylin://ADMIN:KYLIN@10.10.23.25:7070/learn_kylin"

kylin_engine = sa.create_engine(conn_str)

# results = kylin_e ngine.execute('SELECT count(*) FROM KYLIN_SALES')\

print(kylin_engine.table_names())
