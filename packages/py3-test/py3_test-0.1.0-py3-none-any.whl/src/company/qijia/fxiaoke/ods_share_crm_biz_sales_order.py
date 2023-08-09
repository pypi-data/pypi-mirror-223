"""
@Time   : 2019/1/8
@author : lijc210@163.com
@Desc:  : 从分享逍客接口获取销售订单。
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
    account_id = tmp_dict.get("account_id", "")  # 客户名称
    bill_money_to_confirm = tmp_dict.get("bill_money_to_confirm", "")  # 待确认的开票金额
    commision_info = tmp_dict.get("commision_info", "")  # 提成信息
    confirmed_delivery_date = tmp_dict.get("confirmed_delivery_date", "")  # 发货时间
    confirmed_receive_date = tmp_dict.get("confirmed_receive_date", "")  # 收货时间
    delivered_amount_sum = tmp_dict.get("delivered_amount_sum", "")  # 已发货金额
    delivery_comment = tmp_dict.get("delivery_comment", "")  # 发货备注
    delivery_date = tmp_dict.get("delivery_date", "")  # 交货日期
    discount = tmp_dict.get("discount", "")  # 整单折扣
    invoice_amount = tmp_dict.get("invoice_amount", "")  # 已开票金额(元)
    is_user_define_work_flow = tmp_dict.get(
        "is_user_define_work_flow", ""
    )  # 是否是自定义的工作流
    lock_status = tmp_dict.get("lock_status", "")  # 锁定状态
    logistics_status = tmp_dict.get("logistics_status", "")  # 发货状态
    name = tmp_dict.get("name", "")  # 销售订单编号
    new_opportunity_id = tmp_dict.get("new_opportunity_id", "")  # 商机2.0
    opportunity_id = tmp_dict.get("opportunity_id", "")  # 商机名称
    order_amount = tmp_dict.get("order_amount", "")  # 销售订单金额(元)
    order_status = tmp_dict.get("order_status", "")  # 状态
    order_time = ts2dt(tmp_dict.get("order_time", ""))  # 下单日期
    out_resources = tmp_dict.get("out_resources", "")  # 外部来源
    owner = tmp_dict.get("owner", "")  # 负责人
    owner_department = tmp_dict.get("owner_department", "")  # 负责人所在部门
    partner_id = tmp_dict.get("partner_id", "")  # 合作伙伴
    payment_amount = tmp_dict.get("payment_amount", "")  # 已回款金额(元)
    payment_money_to_confirm = tmp_dict.get("payment_money_to_confirm", "")  # 待确认的回款金额
    plan_payment_amount = tmp_dict.get("plan_payment_amount", "")  # 已计划回款金额
    price_book_id = tmp_dict.get("price_book_id", "")  # 价目表
    product_amount = tmp_dict.get("product_amount", "")  # 产品合计
    promotion_id = tmp_dict.get("promotion_id", "")  # 促销活动
    quote_id = tmp_dict.get("quote_id", "")  # 报价单
    receipt_type = tmp_dict.get("receipt_type", "")  # 收款类型
    receivable_amount = tmp_dict.get("receivable_amount", "")  # 待回款金额(元)
    record_type = tmp_dict.get("record_type", "")  # 业务类型
    refund_amount = tmp_dict.get("refund_amount", "")  # 已退款金额(元)
    remark = tmp_dict.get("remark", "")  # 备注
    resource = tmp_dict.get("resource", "")  # 来源
    returned_goods_amount = tmp_dict.get("returned_goods_amount", "")  # 退货单金额(元)
    SalesOrderProductObj = tmp_dict.get("SalesOrderProductObj", "")  # 销售订单产品
    settle_type = tmp_dict.get("settle_type", "")  # 结算方式
    shipping_warehouse_id = tmp_dict.get("shipping_warehouse_id", "")  # 订货仓库
    ship_to_add = tmp_dict.get("ship_to_add", "")  # 收货地址
    ship_to_id = tmp_dict.get("ship_to_id", "")  # 收货人
    ship_to_tel = tmp_dict.get("ship_to_tel", "")  # 收货人电话
    signature_attachment = tmp_dict.get("signature_attachment", "")  # 电子签章附件
    submit_time = ts2dt(tmp_dict.get("submit_time", ""))  # 提交时间
    UDMText1__c = tmp_dict.get("UDMText1__c", "")  # 装修后台链接
    UDSSel1__c = tmp_dict.get("UDSSel1__c", "")  # 装修后台订单状态
    UDSText1__c = tmp_dict.get("UDSText1__c", "")  # 合同编码(非失败订单无需填写)
    UDSText2__c = tmp_dict.get("UDSText2__c", "")  # 商家入驻标示
    _id = tmp_dict.get("_id", "")  # _id
    created_by = tmp_dict.get("created_by", "")  # 创建人
    last_modified_by = tmp_dict.get("last_modified_by", "")  # 最后修改人
    create_time = ts2dt(tmp_dict.get("create_time", ""))  # 创建时间
    last_modified_time = ts2dt(tmp_dict.get("last_modified_time", ""))  # 最后修改时间
    is_deleted = tmp_dict.get("is_deleted", "")  # is_deleted
    out_tenant_id = tmp_dict.get("out_tenant_id", "")  # 外部企业
    out_owner = tmp_dict.get("out_owner", "")  # 外部负责人
    tmp_list = [
        account_id,
        bill_money_to_confirm,
        commision_info,
        confirmed_delivery_date,
        confirmed_receive_date,
        delivered_amount_sum,
        delivery_comment,
        delivery_date,
        discount,
        invoice_amount,
        is_user_define_work_flow,
        lock_status,
        logistics_status,
        name,
        new_opportunity_id,
        opportunity_id,
        order_amount,
        order_status,
        order_time,
        out_resources,
        owner,
        owner_department,
        partner_id,
        payment_amount,
        payment_money_to_confirm,
        plan_payment_amount,
        price_book_id,
        product_amount,
        promotion_id,
        quote_id,
        receipt_type,
        receivable_amount,
        record_type,
        refund_amount,
        remark,
        resource,
        returned_goods_amount,
        SalesOrderProductObj,
        settle_type,
        shipping_warehouse_id,
        ship_to_add,
        ship_to_id,
        ship_to_tel,
        signature_attachment,
        submit_time,
        UDMText1__c,
        UDSSel1__c,
        UDSText1__c,
        UDSText2__c,
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
        apiName="SalesOrderObj",
        limit=100,
        offset=0,
        startTime=startTime,
        endTime=endTime,
    )

    if platform.system() == "Windows":
        filename = "ods_share_crm_biz_sales_order_{}.txt".format(dt)  # 本地测试用
    else:
        filename = "/data/file/share/ods_share_crm_biz_sales_order_{}.txt".format(dt)

    f1 = open(filename, "w", encoding="utf-8")

    for tmp_dict in datas:
        tmp_list1 = biz_leads_field(tmp_dict, dt)
        f1.write("\001".join(tmp_list1) + "\n")

    f1.close()

    if platform.system() != "Windows":
        # 数据put到hadoop
        hdfs_path = "/ods/ods_share_crm_biz_sales_order/dt={0}/ods_share_crm_biz_sales_order_{0}.txt".format(
            dt
        )
        upload_path = hdfs_client.upload(hdfs_path, filename)
        print(upload_path)
        hive_client.execute_with_retry(
            "alter table dw.ods_share_crm_biz_sales_order drop if exists partition (dt='{}')".format(
                dt
            )
        )
        hive_client.execute_with_retry(
            "alter table dw.ods_share_crm_biz_sales_order add partition (dt='{0}') location '/ods/ods_share_crm_biz_sales_order/dt={0}'".format(
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
