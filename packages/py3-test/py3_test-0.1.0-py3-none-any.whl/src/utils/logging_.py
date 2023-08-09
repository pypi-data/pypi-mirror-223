"""
@Time   : 2018/8/28
@author : lijc210@163.com
@Desc:  : 功能描述。
"""
import logging
from logging.handlers import TimedRotatingFileHandler


def FileHandler_(
    getLogger=None,
    setLevel="logging.INFO",
    filename="",
    mode="w",
    StreamHandler=False,
    formatter=None,
):
    """
    日志写入到文件
    :param setLevel:
    :param filename:
    :param mode:
    :param StreamHandler:
    :return:
    """
    logger = logging.getLogger(getLogger)  # 创建logger
    logger.setLevel(eval(setLevel))  # DEBUG输出调试日志，INFO则不输出日志
    if formatter is None:
        formatter = logging.Formatter(
            fmt="[%(asctime)s] %(levelname)s %(filename)s[%(lineno)d]: %(message)s"
        )
    else:
        formatter = logging.Formatter(fmt="%(message)s")

    fh = logging.FileHandler(filename, encoding="utf-8", mode=mode)  # 用于输出到文件
    fh.setFormatter(formatter)
    logger.addHandler(fh)  # 用于输出到文件

    if StreamHandler:
        hdr = logging.StreamHandler()  # 用于输出到控制台
        hdr.setFormatter(formatter)
        logger.addHandler(hdr)  # 用于输出到控制台
    return logger


def TimedRotatingFileHandler_(
    getLogger=None,
    setLevel="logging.INFO",
    filename="",
    interval=1,
    when="MIDNIGHT",
    backupCount=7,
    formatter=None,
):
    """
    日志文件按时间滚动，到了滚动时间必须要有日志写入，才能及时滚动
    :param setLevel:
    :param filename:
    :param interval:
    :param when:
    :param backupCount:
    :return:
    """
    logger = logging.getLogger(getLogger)  # 创建logger
    logger.setLevel(eval(setLevel))  # DEBUG输出调试日志，INFO则不输出日志
    if formatter is None:
        formatter = logging.Formatter(
            fmt="[%(asctime)s] %(levelname)s %(filename)s[%(lineno)d]: %(message)s"
        )
    else:
        formatter = logging.Formatter(fmt="%(message)s")

    fh = TimedRotatingFileHandler(
        filename,
        encoding="utf-8",
        interval=interval,
        when=when,
        backupCount=backupCount,
    )  # 用于输出到文件
    fh.setFormatter(formatter)
    logger.addHandler(fh)  # 用于输出到文件

    return logger


def ConcurrentRotatingFileHandler_():
    """
    多进程日志
    :return:
    """
    pass
