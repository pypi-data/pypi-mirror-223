"""
@Time   : 2019/1/8
@author : lijc210@163.com
@Desc:  : 从分享逍客接口获取销售记录。
"""
import calendar
import platform
import sys
import time
from datetime import date, datetime, timedelta
from multiprocessing.dummy import Pool as ThreadPool

from fxiaoke import Fxiaoke
from hdfs_client import HdfsClient
from pyhive_client import HiveClient

hdfs_client = HdfsClient(host="http://10.10.23.11:50070", user="hadoop")
hive_client = HiveClient(host="10.10.23.11", port=10000, username="hadoop")


def ts2dt(ts):
    """
    时间戳转时间
    :param ts: 1519960417
    :return: datetime str
    """
    ts_len = len(str(int(ts)))
    if ts_len == 13:
        return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(ts / 1000))
    elif ts_len == 11:
        return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(ts))
    else:
        return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(0))


def firstDay_lastDay(dt=None, infmt="%Y-%m-%d %H:%M:%S", outfmt="%Y-%m-%d %H:%M:%S"):
    """
    获取指定时间的月份第一天和最后一天日期
    :return:
    """
    year = time.strptime(dt, infmt).tm_year
    month = time.strptime(dt, infmt).tm_mon
    firstDayWeekDay, monthRange = calendar.monthrange(year, month)  # 第一天的星期和当月的总天数
    firstDay = date(year=year, month=month, day=1).strftime(outfmt)
    lastDay = date(year=year, month=month, day=monthRange).strftime(outfmt)
    return firstDay, lastDay


def sales_recorder_field(tmp_dict, name, dataId, mt):
    """
    销售记录数据字段
    :param tmp_dict:
    :return:
    """
    _id = tmp_dict.get("id", "")  # 销售记录Id
    createTime = ts2dt(tmp_dict.get("createTime", ""))  # 创建时间
    creatorOpenUserId = tmp_dict.get("creatorOpenUserId", "")  # 创建人
    content = tmp_dict.get("content", "")  # 内容

    tmp_list = [_id, createTime, creatorOpenUserId, content, name, dataId, mt]
    tmp_list = [x if isinstance(x, str) else str(x) for x in tmp_list]
    tmp_list = [x.replace("\n", "") for x in tmp_list]
    return tmp_list


def outside_attendance(mt=None):
    """
    获取所有员工的外勤，一次请只获取一天数据，默认昨天
    :return:
    """
    if mt is None:
        mt = time.strftime("%Y%m", time.localtime(time.time()))  # 默认当月

    first_day, last_day = firstDay_lastDay(dt=mt, infmt="%Y%m", outfmt="%Y-%m-%d")
    startTime = (
        int(time.mktime(time.strptime(first_day + " 00:00:00", "%Y-%m-%d %H:%M:%S")))
        * 1000
    )
    endTime = (
        int(time.mktime(time.strptime(last_day + " 23:59:59", "%Y-%m-%d %H:%M:%S")))
        * 1000
    )
    print(startTime, endTime)

    if platform.system() == "Windows":
        kaoqin_filename = "ods_share_crm_sales_recorder_{}.txt".format(mt)  # 本地测试用
        dataId_set = set()
        with open("ods_share_crm_sales_recorder.txt", encoding="utf-8") as f:
            for line in f.readlines():
                dataId_set.add(line.strip())
    else:
        kaoqin_filename = (
            "/data/file/share/ods_share_crm_sales_recorder_{}.txt".format(mt)
        )
        sql = """select DISTINCT index_id from dw.ods_share_crm_biz_leads"""
        dataId_set = {row[0] for row in hive_client.query(sql)}

    f1 = open(kaoqin_filename, "w", encoding="utf-8")

    print("线索数：", len(dataId_set))

    post_data_list = [["LeadsObj", dataId, startTime, endTime] for dataId in dataId_set]

    start = time.time()
    pool = ThreadPool(5)
    res = pool.starmap(fxiaoke.get_crm_salesRecorder_list, post_data_list)
    pool.close()
    pool.join()

    print(time.time() - start)
    # print("res",json.dumps(res))
    salesRecorderTypes = fxiaoke.get_crm_sales_recorder_type()
    sales_id_type_dict = {}
    for adict in salesRecorderTypes:
        _id = adict["id"]
        name = adict["name"]
        if name in ["电话拜访"]:
            sales_id_type_dict[_id] = name

    date_list = []
    for salesRecorders in res:
        for adict in salesRecorders:
            # print(json.dumps(salesRecorders))
            sales_type_id = adict.get("salesRecorderType")
            dataId = adict.get("dataId")
            if sales_type_id in sales_id_type_dict:
                name = sales_id_type_dict[sales_type_id]
                recorder_id = adict["id"]
                date_list.append([recorder_id, name, dataId])

    # print("date_list",date_list)

    for recorder_id, name, dataId in date_list:
        # print(recorder_id)
        salesRecorder = fxiaoke.get_crm_salesRecorder_get(salesRecorderId=recorder_id)
        tmp_list1 = sales_recorder_field(salesRecorder, name, dataId, mt)
        f1.write("\001".join(tmp_list1) + "\n")

    f1.close()

    if platform.system() != "Windows":
        # 数据put到hadoop
        hdfs_path = "/ods/ods_share_crm_sales_recorder/mt={0}/ods_share_crm_sales_recorder_{0}.txt".format(
            mt
        )
        upload_path = hdfs_client.upload(hdfs_path, kaoqin_filename)
        hive_client.execute_with_retry(
            "alter table dw.ods_share_crm_sales_recorder drop if exists partition (mt='{}')".format(
                mt
            )
        )
        hive_client.execute_with_retry(
            "alter table dw.ods_share_crm_sales_recorder add partition (mt='{0}') location '/ods/ods_share_crm_sales_recorder/mt={0}'".format(
                mt
            )
        )
        print(upload_path)


if __name__ == "__main__":
    appId = "FSAID_1317aeb"
    appSecret = "ce9a9bd5dc86464a8aab52582d1bcd9f"
    permanentCode = "3EE9EF73B5BADC079E6646A74FF16610"
    fxiaoke = Fxiaoke(appId=appId, appSecret=appSecret, permanentCode=permanentCode)

    mt = (datetime.now() + timedelta(days=-1)).strftime("%Y%m")  # 默认昨天

    if len(sys.argv) == 2 and len(sys.argv[1]) == 6:
        mt = sys.argv[1]
        print("获取{}数据".format(mt))
    elif len(sys.argv) == 1:
        print("获取{}数据".format(mt))
    else:
        print("[ERROR]只接收一个年月参数，格式YYYYMM")
        sys.exit(1)

    outside_attendance(mt)
