"""
@Time   : 2019/1/8
@author : lijc210@163.com
@Desc:  : 从分享逍客接口获取数据。
"""
import json

import requests
from hdfs_client import HdfsClient
from pyhive_client import HiveClient
from retry import retry

hdfs_client = HdfsClient(host="http://10.10.23.11:50070", user="hadoop")
hive_client = HiveClient(host="10.10.23.11", port=10000, username="hadoop")


@retry(tries=3, delay=2)  # 报错重试
def get(url):
    res = requests.get(url, timeout=20)
    # print (url,res.status_code)
    return res


@retry(tries=3, delay=2)  # 报错重试
def post(url, data=None, json=None):
    res = requests.post(url, data=data, json=json, timeout=20)
    # print (url,res.status_code)
    return res


class Fxiaoke:
    def __init__(self, appId=None, appSecret=None, permanentCode=None):
        self.appId = appId
        self.appSecret = appSecret
        self.permanentCode = permanentCode
        self.corpAccessToken, self.corpId = self.gettoken()

    def gettoken(self):
        """
        获取token
        :return:
        """
        post_data = {
            "appId": self.appId,
            "appSecret": self.appSecret,
            "permanentCode": self.permanentCode,
        }
        resp = post(
            "https://open.fxiaoke.com/cgi/corpAccessToken/get/V2", json=post_data
        )
        resp_dict = resp.json()
        corpAccessToken = resp_dict["corpAccessToken"]
        corpId = resp_dict["corpId"]
        return corpAccessToken, corpId

    def get_department_list(self):
        """
        获取部门列表
        :return:
        """
        post_data = {"corpAccessToken": self.corpAccessToken, "corpId": self.corpId}
        resp_dict = post(
            "https://open.fxiaoke.com/cgi/department/list", json=post_data
        ).json()
        # print(resp_dict)
        return resp_dict["departments"]

    def get_user_simpleList(self, departmentId=None):
        """
        获取部门下成员信息(简略)
        :return:
        """
        post_data = {
            "corpAccessToken": self.corpAccessToken,
            "corpId": self.corpId,
            "departmentId": departmentId,
            "fetchChild": True,
        }
        # print(post_data)
        resp_dict = post(
            "https://open.fxiaoke.com/cgi/user/simpleList", json=post_data
        ).json()
        # print(json.dumps(resp_dict))
        return resp_dict["userList"]

    def get_user_list(self, departmentId=None, departmentName=None):
        """
        获取部门下成员信息(详细)
        :return:
        """
        post_data = {
            "corpAccessToken": self.corpAccessToken,
            "corpId": self.corpId,
            "departmentId": departmentId,
            "fetchChild": True,
            "showDepartmentIdsDetail": True,
        }
        # print(post_data)
        resp_dict = post(
            "https://open.fxiaoke.com/cgi/user/list", json=post_data
        ).json()
        # print(json.dumps(resp_dict))
        userList = []
        for adict in resp_dict["userList"]:
            adict["departmentId"] = departmentId
            adict["departmentName"] = departmentName
            userList.append(adict)
        return userList

    def get_attendance(
        self,
        openUserIds=None,
        pageSize=1000,
        pageNumber=1,
        startTime=None,
        endTime=None,
    ):
        """
        获取考勤数据列表
        :param openUserIds: 被查询人员的openUserId列表；最多支持200人
        :param pageSize: 每页的条数，默认为20 ；最大值为1000
        :param pageNumber:页码，默认为1
        :param startTime:开始时间戳(毫秒)
        :param endTime:结束时间戳(毫秒)；endTime-startTime 不能大于40天
        :return:
        """
        post_data = {
            "corpAccessToken": self.corpAccessToken,
            "corpId": self.corpId,
            "startTime": startTime,
            "endTime": endTime,
            "pageSize": pageSize,
            "pageNumber": pageNumber,
            "openUserIds": openUserIds,
        }
        resp_dict = post(
            "https://open.fxiaoke.com/cgi/attendance/find", json=post_data
        ).json()
        print(resp_dict)
        return resp_dict

    def get_outsideAttendance(
        self,
        openUserIds=None,
        pageSize=1000,
        pageNumber=1,
        startTime=None,
        endTime=None,
    ):
        """
        获取外勤数据列表
        :param openUserIds: 被查询人员的openUserId列表；最多支持200人
        :param pageSize: 每页的条数，默认为20 ；最大值为1000
        :param pageNumber:页码，默认为1
        :param startTime:开始时间戳(毫秒)
        :param endTime:结束时间戳(毫秒)；endTime-startTime 不能大于40天
        :return:
        """
        datas = []
        totalCount = 1000
        # print(pageSize,pageNumber,totalCount)
        while pageSize * (pageNumber - 1) < totalCount:
            post_data = {
                "corpAccessToken": self.corpAccessToken,
                "corpId": self.corpId,
                "startTime": startTime,
                "endTime": endTime,
                "pageSize": pageSize,
                "pageNumber": pageNumber,
                "openUserIds": openUserIds,
            }
            # print(post_data)
            resp_dict = post(
                "https://open.fxiaoke.com/cgi/outsideAttendance/find", json=post_data
            ).json()
            # print(json.dumps(resp_dict))
            totalCount = resp_dict["totalCount"]
            datas.extend(resp_dict["datas"])
            pageNumber += 1
        return datas

    def get_crm_object(self):
        """
        获取企业CRM对象列表(包含预置对象和自定义对象)
        {
            "nickName":"宋玉鹏",
            "name":"宋玉鹏",
            "openUserId":"FSUID_6E94CF1A311BCD0C7FB730B64CD707FF"
        }
        :return:
        """
        post_data = {
            "corpAccessToken": self.corpAccessToken,
            "corpId": self.corpId,
            "currentOpenUserId": "FSUID_6E94CF1A311BCD0C7FB730B64CD707FF",
        }
        resp_dict = post(
            "https://open.fxiaoke.com/cgi/crm/object/list", json=post_data
        ).json()
        print(json.dumps(resp_dict))
        return resp_dict

    def get_crm_object_describe(self, apiName=None):
        """
        获取对象描述
        :return:
        """
        post_data = {
            "corpAccessToken": self.corpAccessToken,
            "corpId": self.corpId,
            "currentOpenUserId": "FSUID_6E94CF1A311BCD0C7FB730B64CD707FF",
            "apiName": apiName,
        }
        resp_dict = post(
            "https://open.fxiaoke.com/cgi/crm/object/describe", json=post_data
        ).json()
        print(json.dumps(resp_dict))
        return resp_dict

    def get_crm_data(
        self, apiName=None, limit=100, offset=0, startTime=None, endTime=None
    ):
        """
        查询对象数据
        :param apiName:对象的api_name
        :param limit:获取数据条数,默认20,最大值为1000(自定义对象最大值为100),过大容易超时
        :param offset:偏移量，从0开始、数值必须为limit的整数倍
        :param startTime:
        :param endTime:
        :return:
        """
        datas = []
        totalNumber = 1000
        # print(pageSize,pageNumber,totalCount)
        n = 0
        while offset - limit < totalNumber:
            n += 1
            post_data = {
                "corpAccessToken": self.corpAccessToken,
                "corpId": self.corpId,
                "currentOpenUserId": "FSUID_6E94CF1A311BCD0C7FB730B64CD707FF",
                "apiName": apiName,
                "searchQuery": {
                    "offset": offset,
                    "limit": limit,
                    "rangeConditions": [
                        {
                            "fieldName": "last_modified_time",
                            "from": startTime,
                            "to": endTime,
                        }
                    ],
                    "orders": [{"ascending": True, "field": "last_modified_time"}],
                },
            }
            # print (post_data)
            resp_dict = post(
                "https://open.fxiaoke.com/cgi/crm/data/query", json=post_data
            ).json()
            # print json.dumps(resp_dict)
            totalNumber = resp_dict["totalNumber"]
            offset = n * limit
            datas.extend(resp_dict["datas"])
        return datas

    def get_crm_salesRecorder_list(
        self,
        apiName=None,
        dataId=None,
        startTime=None,
        endTime=None,
        pageSize=20,
        pageNumber=1,
    ):
        """
        查询销售记录列表
        :param apiName:对象的api_name
        :param limit:获取数据条数,默认20,最大值为1000(自定义对象最大值为100),过大容易超时
        :param offset:偏移量，从0开始、数值必须为limit的整数倍
        :param startTime:
        :param endTime:
        :return:
        """
        total = 1000
        # print(pageSize,pageNumber,total)
        datas = []
        while pageSize * (pageNumber - 1) < total:
            post_data = {
                "corpAccessToken": self.corpAccessToken,
                "corpId": self.corpId,
                "currentOpenUserId": "FSUID_6E94CF1A311BCD0C7FB730B64CD707FF",
                "dataId": dataId,
                "apiName": apiName,
                "startTime": startTime,
                "endTime": endTime,
            }
            # print(post_data)
            resp_dict = post(
                "https://open.fxiaoke.com/cgi/crm/salesRecorder/query", json=post_data
            ).json()
            # print("resp_dict",json.dumps(resp_dict))
            total = resp_dict["total"]
            tmp_list = []
            for adict in resp_dict["salesRecorders"]:
                adict["dataId"] = dataId
                tmp_list.append(adict)
            datas.extend(tmp_list)
            pageNumber += 1
        return datas

    def get_crm_salesRecorder_get(self, salesRecorderId=None):
        """
        获取销售记录详情
        :param salesRecorderId:
        :return:
        """
        post_data = {
            "corpAccessToken": self.corpAccessToken,
            "corpId": self.corpId,
            "currentOpenUserId": "FSUID_6E94CF1A311BCD0C7FB730B64CD707FF",
            "salesRecorderId": salesRecorderId,
        }
        print(post_data)
        resp_dict = post(
            "https://open.fxiaoke.com/cgi/crm/salesRecorder/get", json=post_data
        ).json()
        print(json.dumps(resp_dict, ensure_ascii=False))
        salesRecorder = resp_dict["salesRecorder"]
        return salesRecorder

    def get_crm_sales_recorder_type(self):
        """
        获取销售记录类型
        :return:
        """
        post_data = {
            "corpAccessToken": self.corpAccessToken,
            "corpId": self.corpId,
            "currentOpenUserId": "FSUID_6E94CF1A311BCD0C7FB730B64CD707FF",
        }
        resp_dict = post(
            "https://open.fxiaoke.com/cgi/crm/salesRecorderType/query", json=post_data
        ).json()
        print(json.dumps(resp_dict))
        salesRecorderTypes = resp_dict["salesRecorderTypes"]
        return salesRecorderTypes


if __name__ == "__main__":
    appId = "FSAID_1317aeb"
    appSecret = "ce9a9bd5dc86464a8aab52582d1bcd9f"
    permanentCode = "3EE9EF73B5BADC079E6646A74FF16610"

    fxiaoke = Fxiaoke(appId=appId, appSecret=appSecret, permanentCode=permanentCode)
    # print (fxiaoke.get_department_list())
    # print(json.dumps(fxiaoke.get_user_list(1301)))
    # fxiaoke.get_crm_salesRecorder_list(apiName="LeadsObj")
    fxiaoke.get_crm_sales_recorder_type()

    # fxiaoke.get_crm_object()
    # fields = fxiaoke.get_crm_object_describe(apiName='SalesOrderObj')["objectDesc"]["fields"]
    # for field, tmp_dict in fields.items():
    #     print(field, tmp_dict["label"])
    #
    # startTime = int(time.mktime(time.strptime("20180716", '%Y%m%d'))) * 1000
    # endTime = int(time.mktime(time.strptime("20180717", '%Y%m%d'))) * 1000
    # datas = fxiaoke.get_crm_data(apiName="AccountObj", limit=100, offset=0, startTime=startTime, endTime=endTime)
    # print (json.dumps(datas))
