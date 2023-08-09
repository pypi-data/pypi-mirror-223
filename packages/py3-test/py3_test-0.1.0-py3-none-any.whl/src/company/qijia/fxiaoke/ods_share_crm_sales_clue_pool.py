"""
@Time   : 2019/1/8
@author : lijc210@163.com
@Desc:  : 从分享逍客接口获取线索池。
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


def biz_leads_field(tmp_dict, dt):
    """
    外勤数据字段
    :param tmp_dict:
    :return:
    """
    overtime_hours = tmp_dict.get("overtime_hours", "")  # 超时提醒小时
    assigner_id = tmp_dict.get("assigner_id", "")  # 默认分配人
    is_choose_to_notify = tmp_dict.get("is_choose_to_notify", "")  # 领取线索是否通知线索池管理员
    owner_department = tmp_dict.get("owner_department", "")  # 负责人所在部门
    limit_count = tmp_dict.get("limit_count", "")  # 线索池认领上限
    leads_count = tmp_dict.get("leads_count", "")  # 线索数量
    is_visible_to_member = tmp_dict.get("is_visible_to_member", "")  # 线索池线索是否公开
    name = tmp_dict.get("name", "")  # name
    _id = tmp_dict.get("_id", "")  # _id
    created_by = tmp_dict.get("created_by", "")  # 创建人
    last_modified_by = tmp_dict.get("last_modified_by", "")  # 最后修改人
    create_time = ts2dt(tmp_dict.get("create_time", 0))  # 创建时间
    last_modified_time = ts2dt(tmp_dict.get("last_modified_time", 0))  # 最后修改时间
    is_deleted = tmp_dict.get("is_deleted", "")  # is_deleted
    out_tenant_id = tmp_dict.get("out_tenant_id", "")  # 外部企业
    out_owner = tmp_dict.get("out_owner", "")  # 外部负责人
    tmp_list = [
        overtime_hours,
        assigner_id,
        is_choose_to_notify,
        owner_department,
        limit_count,
        leads_count,
        is_visible_to_member,
        name,
        _id,
        created_by,
        last_modified_by,
        create_time,
        last_modified_time,
        is_deleted,
        out_tenant_id,
        out_owner,
        dt,
    ]
    tmp_list = [x if isinstance(x, str) else str(x) for x in tmp_list]
    tmp_list = [x.replace("\n", "") for x in tmp_list]
    return tmp_list


def crm_biz_leads(dt=None):
    """
    销售线索
    :return:
    """
    yesterday = (datetime.now() + timedelta(days=-1)).strftime("%Y%m%d")  # 默认昨天

    if dt is None:
        dt = yesterday

    startTime = int(time.mktime(time.strptime(dt, "%Y%m%d"))) * 1000
    if dt == yesterday:  # 如果开始时间是昨天，拉取昨天到当前时间的数据
        endTime = int(time.time()) * 1000
    else:
        endTime = startTime + 86400 * 1000
    print(startTime, endTime)

    datas = fxiaoke.get_crm_data(
        apiName="LeadsPoolObj",
        limit=100,
        offset=0,
        startTime=startTime,
        endTime=endTime,
    )

    if platform.system() == "Windows":
        filename = "ods_share_crm_sales_clue_pool_{}.txt".format(dt)  # 本地测试用
    else:
        filename = "/data/file/share/ods_share_crm_sales_clue_pool_{}.txt".format(dt)

    f1 = open(filename, "w", encoding="utf-8")

    for tmp_dict in datas:
        tmp_list1 = biz_leads_field(tmp_dict, dt)
        f1.write("\001".join(tmp_list1) + "\n")

    f1.close()

    if platform.system() != "Windows":
        # 数据put到hadoop
        hdfs_path = "/ods/ods_share_crm_sales_clue_pool/dt={0}/ods_share_crm_sales_clue_pool_{0}.txt".format(
            dt
        )
        upload_path = hdfs_client.upload(hdfs_path, filename)
        print(upload_path)
        hive_client.execute_with_retry(
            "alter table dw.ods_share_crm_sales_clue_pool drop if exists partition (dt='{}')".format(
                dt
            )
        )
        hive_client.execute_with_retry(
            "alter table dw.ods_share_crm_sales_clue_pool add partition (dt='{0}') location '/ods/ods_share_crm_sales_clue_pool/dt={0}'".format(
                dt
            )
        )


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
    crm_biz_leads(dt)
