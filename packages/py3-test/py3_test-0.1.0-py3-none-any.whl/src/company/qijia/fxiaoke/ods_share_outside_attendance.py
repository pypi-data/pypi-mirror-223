"""
@Time   : 2019/1/8
@author : lijc210@163.com
@Desc:  : 从分享逍客接口获取外勤数据。
"""
import platform
import sys
import time
from datetime import datetime, timedelta

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


def outsideAttendance_field(tmp_dict, dt):
    """
    外勤数据字段
    :param tmp_dict:
    :return:
    """
    openUserId = tmp_dict.get("openUserId", "")  # 用户开平账号
    userName = tmp_dict.get("userName", "")  # 用户昵称
    checkinsTimeStamp = tmp_dict.get("checkinsTimeStamp", "")  # 签到时间戳
    checkinsTime = ts2dt(tmp_dict.get("checkinsTimeStamp", ""))  # 签到时间
    checkinsAddressDesc = tmp_dict.get("checkinsAddressDesc", "")  # 外勤签到地址
    customerId = tmp_dict.get("customerId", "")  # 关联客户Id
    contacts = tmp_dict.get("contacts", "")  # 关联联系人列表
    deviceRisk = tmp_dict.get("deviceRisk", "")  # 设备异常: true-异常、false-正常
    contentText = tmp_dict.get("contentText", "")  # 文字描述
    checkinsDistnace = tmp_dict.get("checkinsDistnace", "")  # 签到距离
    # 系统风险: 0- 正常、1- IOS越狱、2- Android 作弊软件、3- Android 伪造地址、4 模拟器、5 root
    cheatRisk = tmp_dict.get("cheatRisk", "")
    checkinsLon = tmp_dict.get("checkinsLon", "")  # 签到经度
    checkinsLat = tmp_dict.get("checkinsLat", "")  # 签到纬度
    tmp_list = [
        openUserId,
        userName,
        checkinsTimeStamp,
        checkinsTime,
        checkinsAddressDesc,
        customerId,
        contacts,
        deviceRisk,
        contentText,
        checkinsDistnace,
        cheatRisk,
        checkinsLon,
        checkinsLat,
        dt,
    ]
    tmp_list = [x if isinstance(x, str) else str(x) for x in tmp_list]
    tmp_list = [x.replace("\n", "") for x in tmp_list]
    return tmp_list


def outside_attendance(dt=None):
    """
    获取所有员工的外勤，一次请只获取一天数据，默认昨天
    :return:
    """
    if dt is None:
        dt = (datetime.now() + timedelta(days=-1)).strftime("%Y-%m-%d %H:%M:%S")  # 默认昨天

    startTime = int(time.mktime(time.strptime(dt, "%Y%m%d"))) * 1000
    endTime = startTime + 86400 * 1000
    print(startTime, endTime)

    if platform.system() == "Windows":
        kaoqin_filename = "ods_share_outside_attendance_{}.txt".format(dt)  # 本地测试用
        openUserId_set = set()
        with open("ods_share_user.txt", encoding="utf-8") as f:
            for line in f.readlines():
                openUserId_set.add(line.strip().split("\001")[0])
    else:
        kaoqin_filename = (
            "/data/file/share/ods_share_outside_attendance_{}.txt".format(dt)
        )
        sql = """select DISTINCT openuserid from dw.ods_share_user  """
        openUserId_set = {row[0] for row in hive_client.query(sql)}

    f1 = open(kaoqin_filename, "w", encoding="utf-8")

    print("员工数：", len(openUserId_set))

    n = 0
    openUserIds = []
    for openUserId in openUserId_set:
        n += 1
        print(n, openUserId)
        openUserIds.append(openUserId)
        if n % 200 == 0:
            datas = fxiaoke.get_outsideAttendance(
                openUserIds=openUserIds,
                pageSize=1000,
                pageNumber=1,
                startTime=startTime,
                endTime=endTime,
            )
            for tmp_dict in datas:
                tmp_list1 = outsideAttendance_field(tmp_dict, dt)
                f1.write("\001".join(tmp_list1) + "\n")
            openUserIds = []  # 重置
            # break

    # 未满200的最后提交一次
    if openUserIds:
        recordresult_all = fxiaoke.get_outsideAttendance(
            openUserIds=openUserIds,
            pageSize=1000,
            pageNumber=1,
            startTime=startTime,
            endTime=endTime,
        )
        for tmp_dict in recordresult_all:
            tmp_list1 = outsideAttendance_field(tmp_dict, dt)
            f1.write("\001".join(tmp_list1) + "\n")

    f1.close()

    if platform.system() != "Windows":
        # 数据put到hadoop
        hdfs_path = "/ods/ods_share_outside_attendance/dt={0}/ods_share_outside_attendance_{0}.txt".format(
            dt
        )
        upload_path = hdfs_client.upload(hdfs_path, kaoqin_filename)
        hive_client.execute_with_retry(
            "alter table dw.ods_share_outside_attendance drop if exists partition (dt='{}')".format(
                dt
            )
        )
        hive_client.execute_with_retry(
            "alter table dw.ods_share_outside_attendance add partition (dt='{0}') location '/ods/ods_share_outside_attendance/dt={0}'".format(
                dt
            )
        )
        print(upload_path)


if __name__ == "__main__":
    appId = "FSAID_1317aeb"
    appSecret = "ce9a9bd5dc86464a8aab52582d1bcd9f"
    permanentCode = "3EE9EF73B5BADC079E6646A74FF16610"
    fxiaoke = Fxiaoke(appId=appId, appSecret=appSecret, permanentCode=permanentCode)

    dt = (datetime.now() + timedelta(days=-1)).strftime("%Y%m%d")  # 默认昨天

    if len(sys.argv) == 2 and len(sys.argv[1]) == 8:
        dt = sys.argv[1]
        print("获取{}数据".format(dt))
    elif len(sys.argv) == 1:
        print("获取{}数据".format(dt))
    else:
        print("[ERROR]只接收一个日期参数，格式YYYYMMDD")
        sys.exit(1)

    outside_attendance(dt)
