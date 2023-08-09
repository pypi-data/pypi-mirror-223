"""
@Time   : 2019/1/8
@author : lijc210@163.com
@Desc:  : 从钉钉接口获取考勤和审批数据，审批依赖考勤。
"""
import calendar
import platform
import sys
import time
from datetime import date, datetime, timedelta

from dingtalk import Dingtalk
from hdfs_client import HdfsClient
from pyhive_client import HiveClient
from try_except_ import try_except

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
    获取指定时间的月份最后一天日期
    :return:
    """
    year = time.strptime(dt, infmt).tm_year
    month = time.strptime(dt, infmt).tm_mon
    firstDayWeekDay, monthRange = calendar.monthrange(year, month)  # 第一天的星期和当月的总天数
    firstDay = date(year=year, month=month, day=1).strftime(outfmt)
    lastDay = date(year=year, month=month, day=monthRange).strftime(outfmt)
    return firstDay, lastDay


def give_day_ops(
    dt=None, dasy=0, infmt="%Y-%m-%d %H:%M:%S", outfmt="%Y-%m-%d %H:%M:%S"
):
    """
    指定日期加减days天
    :param dt: 默认当前时间，2018-03-02 11:13:37
    :param dasy: 1/-1
    :param infmt: '%Y-%m-%d %H:%M:%S'
    :param outfmt: '%Y-%m-%d %H:%M:%S'
    :return: datetime str
    """
    return (datetime.strptime(dt, infmt) + timedelta(days=dasy)).strftime(outfmt)


def kaoqin_field(tmp_dict, mt):
    """
    打卡结果字段
    :param tmp_dict:
    :return:
    """
    _id = tmp_dict.get("id", "")  # 唯一标示ID
    groupId = tmp_dict.get("groupId", "")  # 考勤组ID
    planId = tmp_dict.get("planId", "")  # 排班ID
    recordId = tmp_dict.get("recordId", "")  # 打卡记录ID
    workDate = ts2dt(tmp_dict.get("workDate", ""))  # 工作日
    userId = tmp_dict.get("userId", "")  # 用户ID
    checkType = tmp_dict.get("checkType", "")  # 考勤类型
    # 时间结果,Normal：正常;Early：早退;Late：迟到;SeriousLate：严重迟到；Absenteeism：旷工迟到；NotSigned：未打卡
    timeResult = tmp_dict.get("timeResult", "")
    # 位置结果,Normal：范围内；Outside：范围外；NotSigned：未打卡
    locationResult = tmp_dict.get("locationResult", "")
    # 关联的审批id，当该字段非空时，表示打卡记录与请假、加班等审批有关
    approveId = tmp_dict.get("approveId", "")
    # 关联的审批实例id，当该字段非空时，表示打卡记录与请假、加班等审批有关。可以与 获取单个审批数据配合使用
    procInstId = tmp_dict.get("procInstId", "")
    baseCheckTime = ts2dt(tmp_dict.get("baseCheckTime", ""))  # 计算迟到和早退，基准时间
    userCheckTime = ts2dt(tmp_dict.get("userCheckTime", ""))  # 实际打卡时间
    # 数据来源,ATM：考勤机;BEACON：IBeacon;DING_ATM：钉钉考勤机;APP_USER：用户打卡;APP_BOSS：老板改签;APP_APPROVE：审批系统;SYSTEM：考勤系统;APP_AUTO_CHECK：自动打卡
    sourceType = tmp_dict.get("sourceType", "")
    tmp_list = [
        _id,
        groupId,
        planId,
        recordId,
        workDate,
        userId,
        checkType,
        timeResult,
        locationResult,
        approveId,
        procInstId,
        baseCheckTime,
        userCheckTime,
        sourceType,
        mt,
    ]
    tmp_list = [x if isinstance(x, str) else str(x) for x in tmp_list]
    tmp_list = [x.replace("\n", "") for x in tmp_list]
    return tmp_list


@try_except
def ods_dingtalk_kaoqi(mt=None):
    """
    获取所有员工指定月份的考勤
    :return:
    """
    if mt is None:
        mt = time.strftime("%Y%m", time.localtime(time.time()))  # 默认当月

    first_day, last_day = firstDay_lastDay(dt=mt, infmt="%Y%m", outfmt="%Y-%m-%d")

    workDateFrom = first_day + " 00:00:00"
    workDateTo = (
        give_day_ops(dt=first_day, dasy=6, infmt="%Y-%m-%d", outfmt="%Y-%m-%d")
        + " 23:59:59"
    )
    workDateToLast = last_day + " 23:59:59"

    if platform.system() == "Windows":
        kaoqin_filename = "ods_dingtalk_kaoqin_{}.txt".format(mt)  # 本地测试用
        userid_set = set()
        with open("ods_dingtalk_user.txt", encoding="utf-8") as f:
            for line in f.readlines():
                userid_set.add(line.strip().split("\001")[0])
    else:
        kaoqin_filename = "/data/file/dingtalk/ods_dingtalk_kaoqin_{}.txt".format(mt)
        sql = """select DISTINCT userid from dw.ods_dingtalk_user"""
        userid_set = {row[0] for row in hive_client.query(sql)}

    print("员工数：", len(userid_set))

    workDateList = []
    workDateList.append((workDateFrom, workDateTo))
    while (
        give_day_ops(
            dt=workDateTo, dasy=7, infmt="%Y-%m-%d %H:%M:%S", outfmt="%Y-%m-%d %H:%M:%S"
        )
        < workDateToLast
    ):
        # print("workDateFrom:", workDateFrom)
        # print("workDateTo:", workDateTo)
        workDateFrom = give_day_ops(
            dt=workDateFrom,
            dasy=7,
            infmt="%Y-%m-%d %H:%M:%S",
            outfmt="%Y-%m-%d %H:%M:%S",
        )
        workDateTo = give_day_ops(
            dt=workDateTo, dasy=7, infmt="%Y-%m-%d %H:%M:%S", outfmt="%Y-%m-%d %H:%M:%S"
        )
        workDateList.append((workDateFrom, workDateTo))
    else:
        # print("workDateFrom", workDateFrom)
        # print("workDateTo", workDateTo)
        workDateFrom = give_day_ops(
            dt=workDateFrom,
            dasy=7,
            infmt="%Y-%m-%d %H:%M:%S",
            outfmt="%Y-%m-%d %H:%M:%S",
        )
        workDateTo = workDateToLast
        # print("workDateFrom", workDateFrom)
        # print("workDateTo", workDateTo)
        workDateList.append((workDateFrom, workDateTo))

    with open(kaoqin_filename, "w", encoding="utf-8") as f1:
        for workDateFrom, workDateTo in workDateList:
            print(workDateFrom, workDateTo)
            n = 0
            userIdList = []
            for userid in userid_set:
                n += 1
                print(n, userid)
                userIdList.append(userid)
                if n % 50 == 0:
                    recordresult_all = dingtalk.get_attendance_list(
                        workDateFrom=workDateFrom,
                        workDateTo=workDateTo,
                        userIdList=userIdList,
                        offset=0,
                        limit=50,
                    )
                    for tmp_dict in recordresult_all:
                        tmp_list1 = kaoqin_field(tmp_dict, mt)
                        f1.write("\001".join(tmp_list1) + "\n")
                    userIdList = []  # 重置
                    # break

            # 未满50的最后提交一次
            if userIdList:
                recordresult_all = dingtalk.get_attendance_list(
                    workDateFrom=workDateFrom,
                    workDateTo=workDateTo,
                    userIdList=userIdList,
                    offset=0,
                    limit=50,
                )
                for tmp_dict in recordresult_all:
                    tmp_list1 = kaoqin_field(tmp_dict, mt)
                    f1.write("\001".join(tmp_list1) + "\n")

    if platform.system() != "Windows":
        # 数据put到hadoop
        hdfs_path = (
            "/ods/ods_dingtalk_kaoqin/mt={0}/ods_dingtalk_kaoqin_{0}.txt".format(mt)
        )
        upload_path = hdfs_client.upload(hdfs_path, kaoqin_filename)
        print(upload_path)
        hive_client.execute_with_retry(
            "alter table dw.ods_dingtalk_kaoqin drop if exists partition (mt='{}')".format(
                mt
            )
        )
        hive_client.execute_with_retry(
            "alter table dw.ods_dingtalk_kaoqin add partition (mt='{0}') location '/ods/ods_dingtalk_kaoqin/mt={0}'".format(
                mt
            )
        )


if __name__ == "__main__":
    # 测试账号
    # corpid='dingl1wocjyjz34fowkm'
    # corpsecret='2VB26Ar7iwRx59iFDqZT0yDoeg8wOimumZr80HwFh0PuBY7EkLpR-RiHTDMweRK8'
    corpid = "dingqhzfnaiwaxyzg1dk"
    corpsecret = "OQq7kn5qa3Tmn5H0_YUxeOfmbQ4wG2Mi3f7Qv-nTNLuDD8POP7iDSbeU6LxDBO4F"
    dingtalk = Dingtalk(corpid=corpid, corpsecret=corpsecret)
    # print(dingtalk.get_user(userid="1517464824278718"))
    # process_instance = dingtalk.get_processinstance(process_instance_id="5692dffa-488e-4f4d-9dd5-d86177e32d1f")[
    #     "process_instance"]
    # print(dingtalk.instance_field(process_instance))
    # print(json.dumps(process_instance))
    mt = time.strftime("%Y%m", time.localtime(time.time()))  # 默认当月

    if len(sys.argv) == 2 and len(sys.argv[1]) == 6:
        dt = sys.argv[1]
        print("获取{}数据".format(mt))
    elif len(sys.argv) == 1:
        print("获取{}数据".format(mt))
    else:
        print("[ERROR]只接收一个年月参数，格式YYYYMM")
        sys.exit(1)
    ods_dingtalk_kaoqi(mt)
