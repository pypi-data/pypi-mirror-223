"""
@Time   : 2019/1/8
@author : lijc210@163.com
@Desc:  : 从分享逍客接口获取销售线索。
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
    account_id = tmp_dict.get("account_id", "")  # 客户
    address = tmp_dict.get("address", "")  # 地址
    assigned_time = tmp_dict.get("assigned_time", "")  # 分配时间
    assigner_id = tmp_dict.get("assigner_id", "")  # 分配管理员
    back_reason = tmp_dict.get("back_reason", "")  # 销售人员退回原因
    close_reason = tmp_dict.get("close_reason", "")  # 线索无效原因
    company = tmp_dict.get("company", "")  # 公司
    completed_result = tmp_dict.get("completed_result", "")  # 处理结果
    contact_id = tmp_dict.get("contact_id", "")  # 联系人
    department = tmp_dict.get("department", "")  # 部门
    email = tmp_dict.get("email", "")  # 邮件
    is_overtime = tmp_dict.get("is_overtime", "")  # 是否超时
    job_title = tmp_dict.get("job_title", "")  # 职务
    last_follower = tmp_dict.get("last_follower", "")  # 最后跟进人
    last_follow_time = ts2dt(tmp_dict.get("last_follow_time", 0))  # 最后跟进时间
    leads_pool_id = tmp_dict.get("leads_pool_id", "")  # 线索池
    leads_status = tmp_dict.get("leads_status", "")  # 状态
    lock_status = tmp_dict.get("lock_status", "")  # 锁定状态
    marketing_event_id = tmp_dict.get("marketing_event_id", "")  # 市场活动
    mobile = tmp_dict.get("mobile", "")  # 手机
    name = tmp_dict.get("name", "")  # 姓名
    new_opportunity_id = tmp_dict.get("new_opportunity_id", "")  # 商机2.0
    opportunity_id = tmp_dict.get("opportunity_id", "")  # 商机
    out_resources = tmp_dict.get("out_resources", "")  # 外部来源
    owner = tmp_dict.get("owner", "")  # 负责人
    owner_change_time = tmp_dict.get("owner_change_time", "")  # 负责人变更时间
    owner_department = tmp_dict.get("owner_department", "")  # 负责人所在部门
    partner_id = tmp_dict.get("partner_id", "")  # 合作伙伴
    picture_path = tmp_dict.get("picture_path", "")  # 名片
    record_type = tmp_dict.get("record_type", "")  # 业务类型
    remark = tmp_dict.get("remark", "")  # 销售线索详情
    source = tmp_dict.get("source", "")  # 来源
    tel = tmp_dict.get("tel", "")  # 电话
    transform_time = ts2dt(tmp_dict.get("transform_time", 0))  # 转换时间
    UDDate1__c = tmp_dict.get("UDDate1__c", "")  # 报名日期
    UDDate2__c = tmp_dict.get("UDDate2__c", "")  # 回访时间
    UDLookUp1__c = tmp_dict.get("UDLookUp1__c", "")  # 最近回访人
    UDMSel1__c = tmp_dict.get("UDMSel1__c", "")  # 接单类型
    UDMSel2__c = tmp_dict.get("UDMSel2__c", "")  # 接单房型
    UDMSel3__c = tmp_dict.get("UDMSel3__c", "")  # 接单区域
    UDMText1__c = tmp_dict.get("UDMText1__c", "")  # 跟进备注
    UDSSel1__c = tmp_dict.get("UDSSel1__c", "")  # 线上最近回访结果
    UDSSel2__c = tmp_dict.get("UDSSel2__c", "")  # 线下最近跟进结果
    UDSSel3__c = tmp_dict.get("UDSSel3__c", "")  # 反馈结果
    UDSSel4__c = tmp_dict.get("UDSSel4__c", "")  # 跟进线索标识
    UDSSel5__c = tmp_dict.get("UDSSel5__c", "")  # 是否有入驻信息
    UDSSel6__c = tmp_dict.get("UDSSel6__c", "")  # 店铺入驻意向
    UDSSel7__c = tmp_dict.get("UDSSel7__c", "")  # 是否年后联系
    UDSText1__c = tmp_dict.get("UDSText1__c", "")  # 客服人员
    UDSText3__c = tmp_dict.get("UDSText3__c", "")  # 业务线
    UDSText4__c = tmp_dict.get("UDSText4__c", "")  # 想要入住城市
    UDSText5__c = tmp_dict.get("UDSText5__c", "")  # 公司资质
    UDSText6__c = tmp_dict.get("UDSText6__c", "")  # 公司主营业务
    UDSText9__c = tmp_dict.get("UDSText9__c", "")  # 公司地址
    url = tmp_dict.get("url", "")  # 网址
    _id = tmp_dict.get("_id", "")  # _id
    created_by = tmp_dict.get("created_by", "")  # 创建人
    last_modified_by = tmp_dict.get("last_modified_by", "")  # 最后修改人
    create_time = ts2dt(tmp_dict.get("create_time", 0))  # 创建时间
    last_modified_time = ts2dt(tmp_dict.get("last_modified_time", 0))  # 最后修改时间
    is_deleted = tmp_dict.get("is_deleted", "")  # is_deleted
    out_tenant_id = tmp_dict.get("out_tenant_id", "")  # 外部企业
    out_owner = tmp_dict.get("out_owner", "")  # 外部负责人
    tmp_list = [
        account_id,
        address,
        assigned_time,
        assigner_id,
        back_reason,
        close_reason,
        company,
        completed_result,
        contact_id,
        department,
        email,
        is_overtime,
        job_title,
        last_follower,
        last_follow_time,
        leads_pool_id,
        leads_status,
        lock_status,
        marketing_event_id,
        mobile,
        name,
        new_opportunity_id,
        opportunity_id,
        out_resources,
        owner,
        owner_change_time,
        owner_department,
        partner_id,
        picture_path,
        record_type,
        remark,
        source,
        tel,
        transform_time,
        UDDate1__c,
        UDDate2__c,
        UDLookUp1__c,
        UDMSel1__c,
        UDMSel2__c,
        UDMSel3__c,
        UDMText1__c,
        UDSSel1__c,
        UDSSel2__c,
        UDSSel3__c,
        UDSSel4__c,
        UDSSel5__c,
        UDSSel6__c,
        UDSSel7__c,
        UDSText1__c,
        UDSText3__c,
        UDSText4__c,
        UDSText5__c,
        UDSText6__c,
        UDSText9__c,
        url,
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
        apiName="LeadsObj", limit=100, offset=0, startTime=startTime, endTime=endTime
    )

    if platform.system() == "Windows":
        filename = "ods_share_crm_biz_leads_{}.txt".format(dt)  # 本地测试用
    else:
        filename = "/data/file/share/ods_share_crm_biz_leads_{}.txt".format(dt)

    f1 = open(filename, "w", encoding="utf-8")

    for tmp_dict in datas:
        tmp_list1 = biz_leads_field(tmp_dict, dt)
        f1.write("\001".join(tmp_list1) + "\n")

    f1.close()

    if platform.system() != "Windows":
        # 数据put到hadoop
        hdfs_path = "/ods/ods_share_crm_biz_leads/dt={0}/ods_share_outside_attendance_{0}.txt".format(
            dt
        )
        upload_path = hdfs_client.upload(hdfs_path, filename)
        print(upload_path)
        hive_client.execute_with_retry(
            "alter table dw.ods_share_crm_biz_leads drop if exists partition (dt='{}')".format(
                dt
            )
        )
        hive_client.execute_with_retry(
            "alter table dw.ods_share_crm_biz_leads add partition (dt='{0}') location '/ods/ods_share_crm_biz_leads/dt={0}'".format(
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
