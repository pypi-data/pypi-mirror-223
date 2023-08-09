"""
@Time   : 2019/1/8
@author : lijc210@163.com
@Desc:  : 从分享逍客接口获取客户。
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


def biz_account_field(tmp_dict, dt):
    """
    外勤数据字段
    :param tmp_dict:
    :return:
    """
    account_level = tmp_dict.get("account_level", "")  # 客户级别
    account_no = tmp_dict.get("account_no", "")  # 客户编号
    account_source = tmp_dict.get("account_source", "")  # 来源
    account_status = tmp_dict.get("account_status", "")  # 客户状态
    account_type = tmp_dict.get("account_type", "")  # 客户类型
    address = tmp_dict.get("address", "")  # 详细地址
    area_location = tmp_dict.get("area_location", "")  # 地区定位
    back_reason = tmp_dict.get("back_reason", "")  # 销售人员退回原因
    city = tmp_dict.get("city", "")  # 市
    completion_rate = tmp_dict.get("completion_rate", "")  # 客户资料完善度
    country = tmp_dict.get("country", "")  # 国家
    deal_status = tmp_dict.get("deal_status", "")  # 成交状态
    district = tmp_dict.get("district", "")  # 区
    email = tmp_dict.get("email", "")  # 邮件
    fax = tmp_dict.get("fax", "")  # 传真
    filling_checker_id = tmp_dict.get("filling_checker_id", "")  # 报备审核人
    high_seas_id = tmp_dict.get("high_seas_id", "")  # 公海
    high_seas_name = tmp_dict.get("high_seas_name", "")  # 所属公海
    industry_level1 = tmp_dict.get("industry_level1", "")  # 1级行业
    industry_level2 = tmp_dict.get("industry_level2", "")  # 2级行业
    is_remind_recycling = tmp_dict.get("is_remind_recycling", "")  # 是否待回收提醒
    last_deal_closed_amount = tmp_dict.get(
        "last_deal_closed_amou", ""
    )  # nt                             最后一次成交金额
    last_deal_closed_time = ts2dt(tmp_dict.get("last_deal_closed_time", 0))  # 最后一次成交时间
    last_followed_time = ts2dt(tmp_dict.get("last_followed_time", 0))  # 最后跟进时间
    location = tmp_dict.get("location", "")  # 定位
    lock_status = tmp_dict.get("lock_status", "")  # 锁定状态
    name = tmp_dict.get("name", "")  # 客户名称
    out_resources = tmp_dict.get("out_resources", "")  # 外部来源
    owner = tmp_dict.get("owner", "")  # 负责人
    owner_department = tmp_dict.get("owner_department", "")  # 负责人主属部门
    partner_id = tmp_dict.get("partner_id", "")  # 合作伙伴
    pin_yin = tmp_dict.get("pin_yin", "")  # 名称拼写1
    province = tmp_dict.get("province", "")  # 省
    record_type = tmp_dict.get("record_type", "")  # 业务类型
    recycled_reason = tmp_dict.get("recycled_reason", "")  # 退回/收回原因
    remaining_time = tmp_dict.get("remaining_time", "")  # 剩余保有时间
    remark = tmp_dict.get("remark", "")  # 备注
    tel = tmp_dict.get("tel", "")  # 电话
    total_refund_amount = tmp_dict.get("total_refund_amount", "")  # 退款总额
    transfer_count = tmp_dict.get("transfer_count", "")  # 转手次数
    UDDate1__c = tmp_dict.get("UDDate1__c", "")  # 下次预计拜访时间
    UDInt1__c = tmp_dict.get("UDInt1__c", "")  # 设计师数量(旧)
    UDInt2__c = tmp_dict.get("UDInt2__c", "")  # 队长数量
    UDInt3__c = tmp_dict.get("UDInt3__c", "")  # 展厅数量
    UDMSel1__c = tmp_dict.get("UDMSel1__c", "")  # 接单类型
    UDMSel2__c = tmp_dict.get("UDMSel2__c", "")  # 接单房型
    UDMSel3__c = tmp_dict.get("UDMSel3__c", "")  # 接单区域
    UDMSel4__c = tmp_dict.get("UDMSel4__c", "")  # 合作竞品
    UDMText1__c = tmp_dict.get("UDMText1__c", "")  # 线索跟进备注
    UDMText3__c = tmp_dict.get("UDMText3__c", "")  # 解决办法
    UDSSel10__c = tmp_dict.get("UDSSel10__c", "")  # 展厅规模
    UDSSel11__c = tmp_dict.get("UDSSel11__c", "")  # 设计师规模
    UDSSel12__c = tmp_dict.get("UDSSel12__c", "")  # 每月订单吞吐
    UDSSel13__c = tmp_dict.get("UDSSel13__c", "")  # 竞品订单吞吐
    UDSSel14__c = tmp_dict.get("UDSSel14__c", "")  # 竞品订单转化
    UDSSel15__c = tmp_dict.get("UDSSel15__c", "")  # 客户标识
    UDSSel16__c = tmp_dict.get("UDSSel16__c", "")  # 注册年限
    UDSSel1__c = tmp_dict.get("UDSSel1__c", "")  # 客户当前阶段
    UDSSel2__c = tmp_dict.get("UDSSel2__c", "")  # 未成交原因
    UDSSel3__c = tmp_dict.get("UDSSel3__c", "")  # 客户最新阶段
    UDSSel4__c = tmp_dict.get("UDSSel4__c", "")  # 公司类型
    UDSSel5__c = tmp_dict.get("UDSSel5__c", "")  # 有无拓展店计划
    UDSSel6__c = tmp_dict.get("UDSSel6__c", "")  # 未合作原因
    UDSSel7__c = tmp_dict.get("UDSSel7__c", "")  # 意向分类
    UDSSel8__c = tmp_dict.get("UDSSel8__c", "")  # 年产值
    UDSSel9__c = tmp_dict.get("UDSSel9__c", "")  # 分店数量
    UDSText10__c = tmp_dict.get("UDSText10__c", "")  # 展厅规模（旧）
    UDSText11__c = tmp_dict.get("UDSText11__c", "")  # 放弃原因
    UDSText1__c = tmp_dict.get("UDSText1__c", "")  # 法人
    UDSText2__c = tmp_dict.get("UDSText2__c", "")  # 注册年限（旧）
    UDSText3__c = tmp_dict.get("UDSText3__c", "")  # 对商家印象
    UDSText4__c = tmp_dict.get("UDSText4__c", "")  # 分店数量（旧）
    UDSText5__c = tmp_dict.get("UDSText5__c", "")  # 竞品平台合作情况（旧）
    UDSText6__c = tmp_dict.get("UDSText6__c", "")  # 年产值（旧）
    UDSText7__c = tmp_dict.get("UDSText7__c", "")  # 每月吞吐情况（旧）
    UDSText8__c = tmp_dict.get("UDSText8__c", "")  # 未成交的原因
    UDSText9__c = tmp_dict.get("UDSText9__c", "")  # 客户问题
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
        account_level,
        account_no,
        account_source,
        account_status,
        account_type,
        address,
        area_location,
        back_reason,
        city,
        completion_rate,
        country,
        deal_status,
        district,
        email,
        fax,
        filling_checker_id,
        high_seas_id,
        high_seas_name,
        industry_level1,
        industry_level2,
        is_remind_recycling,
        last_deal_closed_amount,
        last_deal_closed_time,
        last_followed_time,
        location,
        lock_status,
        name,
        out_resources,
        owner,
        owner_department,
        partner_id,
        pin_yin,
        province,
        record_type,
        recycled_reason,
        remaining_time,
        remark,
        tel,
        total_refund_amount,
        transfer_count,
        UDDate1__c,
        UDInt1__c,
        UDInt2__c,
        UDInt3__c,
        UDMSel1__c,
        UDMSel2__c,
        UDMSel3__c,
        UDMSel4__c,
        UDMText1__c,
        UDMText3__c,
        UDSSel10__c,
        UDSSel11__c,
        UDSSel12__c,
        UDSSel13__c,
        UDSSel14__c,
        UDSSel15__c,
        UDSSel16__c,
        UDSSel1__c,
        UDSSel2__c,
        UDSSel3__c,
        UDSSel4__c,
        UDSSel5__c,
        UDSSel6__c,
        UDSSel7__c,
        UDSSel8__c,
        UDSSel9__c,
        UDSText10__c,
        UDSText11__c,
        UDSText1__c,
        UDSText2__c,
        UDSText3__c,
        UDSText4__c,
        UDSText5__c,
        UDSText6__c,
        UDSText7__c,
        UDSText8__c,
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
        apiName="AccountObj", limit=100, offset=0, startTime=startTime, endTime=endTime
    )

    if platform.system() == "Windows":
        filename = "ods_share_crm_biz_account_{}.txt".format(dt)  # 本地测试用
    else:
        filename = "/data/file/share/ods_share_crm_biz_account_{}.txt".format(dt)

    f1 = open(filename, "w", encoding="utf-8")

    for tmp_dict in datas:
        tmp_list1 = biz_account_field(tmp_dict, dt)
        f1.write("\001".join(tmp_list1) + "\n")

    f1.close()

    if platform.system() != "Windows":
        # 数据put到hadoop
        hdfs_path = "/ods/ods_share_crm_biz_account/dt={0}/ods_share_outside_attendance_{0}.txt".format(
            dt
        )
        upload_path = hdfs_client.upload(hdfs_path, filename)
        print(upload_path)
        hive_client.execute_with_retry(
            "alter table dw.ods_share_crm_biz_account drop if exists partition (dt='{}')".format(
                dt
            )
        )
        hive_client.execute_with_retry(
            "alter table dw.ods_share_crm_biz_account add partition (dt='{0}') location '/ods/ods_share_crm_biz_account/dt={0}'".format(
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
