"""
Created on 2016/5/10
@author: lijc210@163.com
Desc: 功能描述。
"""

# -*- coding:utf-8 -*-

import datetime
import os
import subprocess

from utils.pg_client import PostgreSQL

pg = PostgreSQL()


def pgbak():
    # 要备份的表
    sql = """select table_schema || '.' || table_name AS table_full_name, pg_size_pretty(pg_total_relation_size('"' || table_schema || '"."' || table_name || '"')) AS size
                FROM information_schema.tables
                where table_schema not in('pg_catalog','backup','test','bipangu','data_out','information_schema')
                and table_name not like 'ol_traf%' and table_name not like 'conf_ip_city%'
                and table_name not like 'ol_zx_apply_order%'
                and table_name not like 'fred%' and table_name not like 'ol_crm%' and table_name not like 'ol_tg%'
                and table_name not like 'ol_mail%' and table_name not like 'ol_click%'
                --and (tablename not like '%tmp%' or tablename not like '%test%' or tablename not like '%2016%' or tablename not like '%fred%' or tablename not like '%bak%')
                or (table_schema in ('bipangu') and table_name like '%conf%' )
                or (table_schema in ('data_out') and table_name like 'bi%' )
                order by table_full_name"""
    sqlres = pg.queryBySQL(sql)
    tableList = [row[0] for row in sqlres]
    dt = datetime.datetime.now().strftime("%Y%m%d")
    # 备份目录
    pgdatabakdir = "/data/backup/pgdatabak/{}/".format(dt)
    # 创建备份目录
    if os.path.exists(pgdatabakdir):
        __import__("shutil").rmtree(pgdatabakdir)
    else:
        os.mkdir(pgdatabakdir)
    # 逐个表备份
    for tablename in tableList:
        subprocess.getoutput(
            "/usr/pgsql-9.5/bin/pg_dump -U postgres dw -c -t {0} | gzip > {1}/{0}.sql.gz".format(
                tablename, pgdatabakdir
            )
        )
    # #拷贝到10.10.23.100
    # commands.getoutput("scp -r {0} root@10.10.23.100:/data/backup/pgdatabak/".format(pgdatabakdir))
    # 删除7天前的日期
    dayago = (datetime.datetime.now() + datetime.timedelta(days=-7)).strftime("%Y%m%d")
    dayagobakdir = "/data/backup/pgdatabak/{}".format(dayago)
    if os.path.exists(dayagobakdir):
        __import__("shutil").rmtree(dayagobakdir)
    # #删除10.10.23.100上7天前日期
    # commands.getoutput("ssh root@10.10.23.100 'rm -rf {0}'".format(dayagobakdir))
    # 恢复
    # commands.getoutput("ssh root@10.10.23.100 'sh /data/backup/pgdatabak/recover.sh {0}'".format(dt))


if __name__ == "__main__":
    pgbak()
