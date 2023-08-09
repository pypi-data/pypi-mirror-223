#!/usr/bin/env python
import os

from utils.utils import sqlite3_client

if not os.path.exists("wechat.db"):
    print("重新生成wechat.db")
    sqlite3_client.execute(
        """
            CREATE TABLE quick_reply
           (id   integer PRIMARY KEY autoincrement,
            content   TEXT                )
    """
    )
    sqlite3_client.execute(
        """
            CREATE TABLE user
           (user_name   PRIMARY KEY   NOT NULL ,
            nick_name   CHAR(50)                ,
            remark_name   CHAR(50)                ,
            head_img_url      CHAR(50)               )
    """
    )
    sqlite3_client.execute(
        """
            CREATE TABLE message
           (from_username   CHAR(50)                ,
           to_username   CHAR(50)                ,
           content   TEXT                ,
           msg_type      TINYINT                 ,
           msg_source      TINYINT                 ,
           create_time   INT                )
    """
    )
else:
    print("加载wechat.db完成")
