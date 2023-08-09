from contextlib import closing

from sqlalchemy import create_engine

uri = "clickhouse://ck_readonly:shgqsh2020@114.116.224.81:8123/ads"

engine = create_engine(uri)

with closing(engine.raw_connection()) as conn:
    cursor = conn.cursor()
    cursor.execute("select * from ads_sales_shop_channel_etl limit 2")
    print(cursor.fetchall())
    print(cursor.description)

# session = make_session(engine)

# session.
