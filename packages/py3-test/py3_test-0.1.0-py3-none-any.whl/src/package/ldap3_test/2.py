"""
Created on 2017/6/16 0016
@author: lijc210@163.com
Desc: 功能描述。
"""
import ldap

AUTH_LDAP_SERVER_URI = "ldap://10.240.81.57:389"  # ldap主机
AUTH_LDAP_BIND_DN = "gyldap"  # 根据自己实际需求填写
AUTH_LDAP_BIND_PASSWORD = "hWiYUC!2tuRuCaE!"  # 管理账户密码
SEARCH_BASE = "DC=guoquan,DC=cn"


def ldapAuth(username, password):
    try:
        # 建立连接
        ldapconn = ldap.initialize(AUTH_LDAP_SERVER_URI)
        # 绑定管理账户，用于用户的认证
        ldapconn.simple_bind_s(AUTH_LDAP_BIND_DN, AUTH_LDAP_BIND_PASSWORD)
        searchScope = ldap.SCOPE_SUBTREE  # 指定搜索范围
        searchFilter = "(sAMAccountName=%s)" % username  # 指定搜索字段
        ldap_result_id = ldapconn.search(
            SEARCH_BASE, searchScope, searchFilter, None
        )  # 返回该用户的所有信息，类型列表
        result_type, result_data = ldapconn.result(ldap_result_id, 0)
        if result_data:
            user_dn = result_data[0][0]  # 获取用户的cn,ou,dc
            try:
                ldapconn.simple_bind_s(user_dn, password)  # 对用户的密码进行验证
                print("验证成功")
                return True
            except ldap.LDAPError as e:
                print(e)
                return False
        else:
            return False
    except ldap.LDAPError as e:
        print(e)
        return False


if __name__ == "__main__":
    print(ldapAuth("lijicong", "Sysz0210"))
