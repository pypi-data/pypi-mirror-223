"""
@Time   : 2019/1/8
@author : lijc210@163.com
@Desc:  : 从分享逍客接口获取外勤数据。
"""
import platform
import time
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


def user_field(tmp_dict):
    """
    用户数据字段
    :param tmp_dict:
    :return:
    """
    openUserId = tmp_dict.get("openUserId", "")  # 开放平台员工帐号
    account = tmp_dict.get("account", "")  # 员工账号
    name = tmp_dict.get("name", "")  # 员工姓名
    nickName = tmp_dict.get("nickName", "")  # 员工昵称
    isStop = tmp_dict.get("isStop", "")  # 员工状态，如果为true,则表示此员工离职，否则，该员工状态为在职
    email = tmp_dict.get("email", "")  # 邮箱
    mobile = tmp_dict.get("mobile", "")  # 手机号
    gender = tmp_dict.get("gender", "")  # 员工性别：M(男) F(女)
    position = tmp_dict.get("position", "")  # 员工职位
    profileImageUrl = tmp_dict.get("profileImageUrl", "")  # 头像文件ID
    departmentIds = tmp_dict.get("departmentIds", "")  # 员工所属部门及其父部门ID列表
    mainDepartmentId = tmp_dict.get("mainDepartmentId", "")  # 员工主属部门ID
    attachingDepartmentIds = tmp_dict.get("attachingDepartmentIds", "")  # 员工附属部门ID列表
    employeeNumber = tmp_dict.get("employeeNumber", "")  # 员工编号
    hireDate = tmp_dict.get("hireDate", "")  # 入职日期
    birthDate = tmp_dict.get("birthDate", "")  # 员工生日
    startWorkDate = tmp_dict.get("startWorkDate", "")  # 参加工作日期
    createTime = ts2dt(tmp_dict.get("createTime", ""))  # 创建时间
    leaderId = tmp_dict.get("leaderId	", "")  # 汇报对象
    departmentId = tmp_dict.get("departmentId", "")  # 部门id
    departmentName = tmp_dict.get("departmentName", "")  # 部门名称
    tmp_list = [
        openUserId,
        account,
        name,
        nickName,
        isStop,
        email,
        mobile,
        gender,
        position,
        profileImageUrl,
        departmentIds,
        mainDepartmentId,
        attachingDepartmentIds,
        employeeNumber,
        hireDate,
        birthDate,
        startWorkDate,
        createTime,
        leaderId,
        departmentId,
        departmentName,
    ]
    tmp_list = [x if isinstance(x, str) else str(x) for x in tmp_list]
    tmp_list = [x.replace("\n", "") for x in tmp_list]
    return tmp_list


def ods_share_user():
    """
    获取所有员工信息
    :return:
    """

    departments = fxiaoke.get_department_list()
    departmentId_name_dict = {}
    for i, adict in enumerate(departments):
        _id = adict.get("id", None)
        name = adict.get("name", None)  # 部门名称
        print(i, _id, name)
        departmentId_name_dict[_id] = name
        # if i >= 20:
        #     break

    pool = ThreadPool(5)
    res = pool.starmap(fxiaoke.get_user_list, departmentId_name_dict.items())
    pool.close()
    pool.join()

    if platform.system() == "Windows":
        kaoqin_filename = "ods_share_user.txt"  # 本地测试用
    else:
        kaoqin_filename = "/data/file/share/ods_share_user.txt"

    f1 = open(kaoqin_filename, "w", encoding="utf-8")

    for userlist in res:
        for tmp_dict in userlist:
            tmp_list1 = user_field(tmp_dict)
            f1.write("\001".join(tmp_list1) + "\n")

    if platform.system() != "Windows":
        # 数据put到hadoop
        hdfs_path = "/ods/ods_share_user/ods_share_user.txt"
        upload_path = hdfs_client.upload(hdfs_path, kaoqin_filename)
        print(upload_path)


if __name__ == "__main__":
    appId = "FSAID_1317aeb"
    appSecret = "ce9a9bd5dc86464a8aab52582d1bcd9f"
    permanentCode = "3EE9EF73B5BADC079E6646A74FF16610"
    fxiaoke = Fxiaoke(appId=appId, appSecret=appSecret, permanentCode=permanentCode)
    ods_share_user()
