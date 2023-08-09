"""
@Time   : 2019/1/8
@author : lijc210@163.com
@Desc:  : 从钉钉接口获取考勤和审批数据，审批依赖考勤。
"""
import calendar
import json
import platform
import sys
import time
import traceback
from datetime import date, datetime, timedelta

from dingtalk import Dingtalk
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


def instance_field(procInstId, procInstname, tmp_dict, mt):
    """
    实例详情字段
    :param tmp_dict:
    :return:
    """
    title = tmp_dict.get("title", "").encode("utf-8").decode()  # 审批实例标题
    create_time = tmp_dict.get("create_time", "")  # 开始时间
    finish_time = tmp_dict.get("finish_time", "")  # 结束时间
    originator_userid = tmp_dict.get("originator_userid", "")  # 发起人
    originator_dept_id = tmp_dict.get("originator_dept_id", "")  # 发起部门
    # 审批状态，分为NEW（刚创建） | RUNNING（运行中） | TERMINATED（被终止） | COMPLETED（完成） | CANCELED（取消）
    status = tmp_dict.get("status", "")
    approver_userids = tmp_dict.get("approver_userids", "")  # 审批人
    cc_userids = tmp_dict.get("cc_userids", "")  # 抄送人
    form_component_values_json = tmp_dict.get("form_component_values", "")  # 表单详情列表
    form_component_values = json.dumps(form_component_values_json)  # 表单详情列表
    result = tmp_dict.get("result", "")  # 审批结果，分为 agree 和 refuse
    business_id = tmp_dict.get("business_id", "")  # 审批实例业务编号
    operation_records = json.dumps(tmp_dict.get("operation_records", ""))  # 操作记录列表
    tasks = tmp_dict.get("tasks", "")  # 任务列表
    originator_dept_name = tmp_dict.get("originator_dept_name", "")  # 发起部门
    # 审批实例业务动作，MODIFY表示该审批实例是基于原来的实例修改而来，REVOKE表示该审批实例对原来的实例进行撤销，NONE表示正常发起
    biz_action = tmp_dict.get("biz_action", "")
    # 审批附属实例列表，当已经通过的审批实例被修改或撤销，会生成一个新的实例，作为原有审批实例的附属。如果想知道当前已经通过的审批实例的状态，可以依次遍历它的附属列表，查询里面每个实例的biz_action
    attached_process_instance_ids = tmp_dict.get("attached_process_instance_ids", "")

    ext_value_pushTag = ""
    ext_value_extension_tag = ""
    ext_value_fromTime = 0
    ext_value_toTime = 0
    ext_value_durationInHour = 0

    if procInstname == "请假调休":
        try:
            ext_value = json.loads(form_component_values_json[0]["ext_value"])  # 标签扩展值
            # print(ext_value)
            ext_value_pushTag = ext_value.get("pushTag", "")  # 类型
            ext_value_extension_tag = json.loads(ext_value.get("extension", "{}")).get(
                "tag", ""
            )  # 事由
            detailList = ext_value.get("detailList", [])
            if detailList:
                ext_value_fromTime = ts2dt(
                    detailList[0]["approveInfo"].get("fromTime", 0)
                )  # 开始时间
                ext_value_toTime = ts2dt(
                    detailList[-1]["approveInfo"].get("toTime", 0)
                )  # 结束时间
            else:
                ext_value_fromTime = ts2dt(0)
                ext_value_toTime = ts2dt(0)
            ext_value_durationInHour = ext_value.get("durationInHour", "")  # 持续时间
        except Exception:
            traceback.print_exc()
            print("请假调休", json.dumps(tmp_dict))
    elif procInstname == "补卡申请":
        try:
            for adict in form_component_values_json:
                name = adict.get("name")
                if "原因" in name:
                    ext_value_pushTag = name
                    ext_value_extension_tag = adict.get("value")  # 事由
                if "ext_value" in adict:
                    ext_value = json.loads(adict["ext_value"])
                    planText = ext_value.get("planText")
                    userCheckTime = ext_value.get("userCheckTime", "0")
                    if isinstance(userCheckTime, str):
                        userCheckTime = int(userCheckTime)
                    if "上班" in planText:
                        ext_value_fromTime = ts2dt(userCheckTime)
                    elif "下班" in planText:
                        ext_value_toTime = ts2dt(userCheckTime)
        except Exception:
            traceback.print_exc()
            print("补卡申请", json.dumps(tmp_dict))
    elif procInstname == "加班申请":
        try:
            for adict in form_component_values_json:
                name = adict.get("name")
                value = adict.get("value", "")
                if name == "加班":
                    value_list = json.loads(value)
                    for bdict in value_list:
                        componentName = bdict.get("componentName")
                        extValue = bdict.get("extValue", "")
                        if componentName == "NumberField":
                            extValue_dict = json.loads(extValue)
                            detailList = extValue_dict.get("detailList")
                            ext_value_fromTime = ts2dt(
                                detailList[0]["approveInfo"].get("fromTime", 0)
                            )  # 开始时间
                            ext_value_toTime = ts2dt(
                                detailList[-1]["approveInfo"].get("toTime", 0)
                            )  # 结束时间
                            ext_value_durationInHour = extValue_dict.get(
                                "durationInHour"
                            )  # 持续时间
        except Exception:
            traceback.print_exc()
            print("加班申请", json.dumps(tmp_dict))
    elif procInstname == "外出申请":
        try:
            for adict in form_component_values_json:
                ext_value = adict.get("ext_value")
                if ext_value:
                    ext_value_dict = json.loads(ext_value)
                    ext_value_pushTag = ext_value_dict.get("pushTag", "")  # 类型
                    ext_value_extension_tag = json.loads(
                        ext_value_dict.get("extension", "{}")
                    ).get(
                        "tag", ""
                    )  # 事由
                    detailList = ext_value_dict.get("detailList", [])
                    ext_value_fromTime = ts2dt(
                        detailList[0]["approveInfo"].get("fromTime", 0)
                    )  # 开始时间
                    ext_value_toTime = ts2dt(
                        detailList[-1]["approveInfo"].get("toTime", 0)
                    )  # 结束时间
                    ext_value_durationInHour = ext_value_dict.get(
                        "durationInHour"
                    )  # 持续时间
                    break
        except Exception:
            traceback.print_exc()
            print("外出申请", json.dumps(tmp_dict))
    elif procInstname == "出差申请":
        try:
            for adict in form_component_values_json:
                name = adict.get("name")
                if name == "出差":
                    value = adict.get("value")
                    if value:
                        value_dict = json.loads(value)
                        for blist in value_dict:
                            children = blist.get("children")
                            if children:
                                bvalue = blist.get("value")
                                if bvalue:
                                    bvalue_list = json.loads(bvalue)
                                    for cdict in bvalue_list:
                                        rowValue = cdict.get("rowValue")
                                        if rowValue:
                                            for ddict in rowValue:
                                                label = ddict.get("label")
                                                if label == "时长":
                                                    detailList = ddict["extendValue"][
                                                        "detailList"
                                                    ]
                                                    ext_value_fromTime = ts2dt(
                                                        detailList[0][
                                                            "approveInfo"
                                                        ].get("fromTime", 0)
                                                    )  # 开始时间
                                                    ext_value_toTime = ts2dt(
                                                        detailList[-1][
                                                            "approveInfo"
                                                        ].get("toTime", 0)
                                                    )  # 结束时间
                                                    ext_value_durationInHour = ddict[
                                                        "extendValue"
                                                    ].get(
                                                        "durationInHour"
                                                    )  # 持续时间
                                                    break
                                break
        except Exception:
            traceback.print_exc()
            print("出差申请", json.dumps(tmp_dict))
    else:
        print("没有解析", json.dumps(tmp_dict))
    tmp_list = [
        procInstId,
        procInstname,
        title,
        create_time,
        finish_time,
        originator_userid,
        originator_dept_id,
        status,
        approver_userids,
        cc_userids,
        form_component_values,
        result,
        business_id,
        operation_records,
        tasks,
        originator_dept_name,
        biz_action,
        attached_process_instance_ids,
        ext_value_pushTag,
        ext_value_extension_tag,
        ext_value_fromTime,
        ext_value_toTime,
        ext_value_durationInHour,
        mt,
    ]
    tmp_list = [x if isinstance(x, str) else str(x) for x in tmp_list]
    tmp_list = [x.replace("\n", "") for x in tmp_list]
    return tmp_list


# @try_except
def ods_dingtalk_shenpi(mt=None):
    """
    获取所有员工指定年月的审批数据
    :return:
    """
    if mt is None:
        mt = time.strftime("%Y%m", time.localtime(time.time()))  # 默认当月

    first_day, last_day = firstDay_lastDay(dt=mt, infmt="%Y%m", outfmt="%Y-%m-%d")
    start_time = (
        int(time.mktime(time.strptime(first_day + " 00:00:00", "%Y-%m-%d %H:%M:%S")))
        * 1000
    )
    end_time = (
        int(time.mktime(time.strptime(last_day + " 23:59:59", "%Y-%m-%d %H:%M:%S")))
        * 1000
    )
    start_time, end_time = 1547537195000, 1547796395000
    print(first_day, last_day)
    print(start_time, end_time)

    if platform.system() == "Windows":
        shenpi_filename = "ods_dingtalk_shenpi_{}.txt".format(mt)  # 本地测试用
    else:
        shenpi_filename = "/data/file/dingtalk/ods_dingtalk_shenpi_{}.txt".format(mt)

    process_list = dingtalk.get_process_listbyuserid()  # 获取用户可见的审批模板

    processinstance_dict = {}
    for adict in process_list:
        name = adict.get("name")
        # if name in ("补卡申请","出差申请","加班申请","请假调休","外出申请"):
        # if name in ("补卡申请","出差申请","加班申请","请假调休","外出申请","虚拟币解锁申请"):
        if name in ("补卡申请"):
            process_code = adict.get("process_code")
            processinstance_list = dingtalk.get_processinstance_listids(
                process_code=process_code,
                start_time=start_time,
                end_time=end_time,
                size=10,
                cursor=1,
                userid_list=None,
            )
            print(name, len(processinstance_list))
            for processinstance in processinstance_list:
                processinstance_dict[processinstance] = name

    print("总实例id", len(processinstance_dict))

    with open(shenpi_filename, "w", encoding="utf-8") as f2:
        # all_processinstance_set = set(["fceb1d68-a943-45a1-9aa4-fa699494744c"]) # 测试
        for procInstId, name in processinstance_dict.items():
            print(procInstId)
            process_instance = dingtalk.get_processinstance(
                process_instance_id=procInstId
            )
            tmp_list2 = instance_field(procInstId, name, process_instance, mt)
            f2.write("\001".join(tmp_list2) + "\n")

    if platform.system() != "Windows":
        # 数据put到hadoop

        hdfs_path = (
            "/ods/ods_dingtalk_shenpi/dt={0}/ods_dingtalk_shenpi_{0}.txt".format(mt)
        )
        upload_path = hdfs_client.upload(hdfs_path, shenpi_filename)
        print(upload_path)
        hive_client.execute_with_retry(
            "alter table dw.ods_dingtalk_shenpi drop if exists partition (mt='{}')".format(
                mt
            )
        )
        hive_client.execute_with_retry(
            "alter table dw.ods_dingtalk_shenpi add partition (mt='{0}') location '/ods/ods_dingtalk_shenpi/mt={0}'".format(
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
    mt = (datetime.now() + timedelta(days=-1)).strftime("%Y%m")  # 默认昨天

    if len(sys.argv) == 2 and len(sys.argv[1]) == 6:
        mt = sys.argv[1]
        print("获取{}数据".format(mt))
    elif len(sys.argv) == 1:
        print("获取{}数据".format(mt))
    else:
        print("[ERROR]只接收一个年月参数，格式YYYYMM")
        sys.exit(1)
    ods_dingtalk_shenpi(mt)
