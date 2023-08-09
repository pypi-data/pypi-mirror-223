#!/usr/bin/env python
import os


class Config:
    """
    Basic config
    """

    # Application config
    TIMEZONE = "Asia/Shanghai"
    BASE_DIR = os.path.dirname(os.path.dirname(__file__))
    TEMP_DIR = os.path.join(BASE_DIR, "temp")
    OUT_DIR = os.path.join(BASE_DIR, "out")
    LOG_DIR = os.path.join(BASE_DIR, "log")
    DATA_DIR = os.path.join(BASE_DIR, "data")
    MAIL_DIR = os.path.join(DATA_DIR, "mail")
    SENTRY_URL = "https://43f2ceecdeae48d9a7b83ff801b9de8c@sentry.zzgqsh.com/32"
    if os.path.exists(TEMP_DIR) is False:
        os.mkdir(TEMP_DIR)
    if os.path.exists(OUT_DIR) is False:
        os.mkdir(OUT_DIR)
    if os.path.exists(LOG_DIR) is False:
        os.mkdir(LOG_DIR)
    if os.path.exists(DATA_DIR) is False:
        os.mkdir(DATA_DIR)
    if os.path.exists(MAIL_DIR) is False:
        os.mkdir(MAIL_DIR)
