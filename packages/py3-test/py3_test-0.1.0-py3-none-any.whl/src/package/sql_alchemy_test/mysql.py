"""
@File    :   ck.py
@Time    :   2021/01/08 10:10:26
@Author  :   lijc210@163.com
@Desc    :   None
"""
from sqlalchemy import MetaData, create_engine

engine = create_engine(
    "mysql+pymysql://root:123456@192.168.205.130:3306/test?charset=utf8",
    max_overflow=10,
    echo=True,
)

sql = "select * from testa;"
conn = engine.connect()
res_obj = conn.execute(object_=sql)
print(res_obj.rowcount)

META_DATA = MetaData(bind=engine, reflect=True)

TABLE = META_DATA.reflect(only=["testa"])
print("aaaaaaa", TABLE)

metadata = MetaData()
print(metadata.reflect(engine, only=["testa"]))
