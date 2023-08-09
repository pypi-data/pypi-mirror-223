"""
@Time   : 2019/1/8
@author : lijc210@163.com
@Desc:  : 从钉钉接口获取考勤和审批数据，审批依赖考勤。
"""
import platform

from dingtalk import Dingtalk
from hdfs_client import HdfsClient
from pyhive_client import HiveClient

hdfs_client = HdfsClient(host="http://10.10.23.11:50070", user="hadoop")
hive_client = HiveClient(host="10.10.23.11", port=10000, username="hadoop")


def user_field(tmp_dict, department_id, department_name):
    """
    打卡结果字段
    :param tmp_dict:
    :return:
    """
    userid = tmp_dict.get("userid", "")  # 员工唯一标识ID（不可修改）
    order = tmp_dict.get("order", "")  # 表示人员在此部门中的排序，列表是按order的倒序排列输出的，即从大到小排列输出的
    unionid = tmp_dict.get("unionid", "")  # 在当前isv全局范围内唯一标识一个用户的身份，用户无法修改
    isAdmin = tmp_dict.get("isAdmin", "")  # 是否是企业的管理员，true表示是，false表示不是
    isBoss = tmp_dict.get("isBoss", "")  # 是否为企业的老板，true表示是，false表示不是
    isHide = tmp_dict.get("isHide", "")  # 是否隐藏号码，true表示是，false表示不是
    isLeader = tmp_dict.get("isLeader", "")  # 是否是部门的主管，true表示是，false表示不是
    name = tmp_dict.get("name", "")  # 成员名称
    active = tmp_dict.get("active", "")  # 表示该用户是否激活了钉钉
    department = tmp_dict.get("department", "")  # 成员所属部门id列表
    position = tmp_dict.get("position", "")  # 职位信息
    avatar = tmp_dict.get("avatar", "")  # 头像url
    jobnumber = tmp_dict.get("jobnumber", "")  # 员工工号
    hiredDate = tmp_dict.get("hiredDate", "")  # 入职时间
    mobile = tmp_dict.get("mobile", "")  # 手机号
    tmp_list = [
        userid,
        order,
        unionid,
        isAdmin,
        isBoss,
        isHide,
        isLeader,
        name,
        active,
        department,
        position,
        avatar,
        jobnumber,
        hiredDate,
        department_id,
        department_name,
        mobile,
    ]
    tmp_list = [x if isinstance(x, str) else str(x) for x in tmp_list]
    return tmp_list


def ods_dingtalk_user():
    """
    获取所有员工的考勤与审批数据，一次请只获取一天数据，默认昨天
    :return:
    """

    if platform.system() == "Windows":
        filename = "ods_dingtalk_user.txt"  # 本地测试用
    else:
        filename = "/data/file/dingtalk/ods_dingtalk_user.txt"

    f1 = open(filename, "w", encoding="utf-8")

    department = dingtalk.get_department_list()["department"]  # 获取部门列表
    for adict in department:
        department_id = adict["id"]
        department_name = adict["name"]
        userlist = dingtalk.get_listbypage(
            department_id=department_id
        )  # 获取部门下的所有userid
        for tmp_dict in userlist:
            tmp_list1 = user_field(tmp_dict, department_id, department_name)
            f1.write("\001".join(tmp_list1) + "\n")
    f1.close()

    if platform.system() != "Windows":
        # 数据put到hadoop
        hdfs_path = "/ods/ods_dingtalk_user/ods_dingtalk_user.txt"
        upload_path = hdfs_client.upload(hdfs_path, filename)
        print(upload_path)


if __name__ == "__main__":
    # 测试账号
    # corpid='dingl1wocjyjz34fowkm'
    # corpsecret='2VB26Ar7iwRx59iFDqZT0yDoeg8wOimumZr80HwFh0PuBY7EkLpR-RiHTDMweRK8'
    corpid = "dingqhzfnaiwaxyzg1dk"
    corpsecret = "OQq7kn5qa3Tmn5H0_YUxeOfmbQ4wG2Mi3f7Qv-nTNLuDD8POP7iDSbeU6LxDBO4F"
    dingtalk = Dingtalk(corpid=corpid, corpsecret=corpsecret)
    ods_dingtalk_user()
