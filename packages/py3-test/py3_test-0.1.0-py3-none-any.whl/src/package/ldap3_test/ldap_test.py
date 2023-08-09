"""
Created on 2017/6/16 0016
@author: lijc210@163.com
Desc: 功能描述。
"""
import ldap


def login_ldap(username, password):
    try:
        # print("开始执行"
        # Server = "LDAP://tg.com.local"
        Server = "ldap://10.10.20.154:389"
        # baseDN = "dc=domainname,dc=com"
        baseDN = "dc=tg,dc=com,dc=local"
        # root_dn = cn=admin,dc=qijia,dc=com
        # root_pw = jiacom
        searchScope = ldap.SCOPE_SUBTREE
        # 设置过滤属性，这里只显示cn=test的信息
        searchFilter = "sAMAccountName=" + username
        # 为用户名加上域名
        username = "tg\\" + username
        # None表示搜索所有属性，['cn']表示只搜索cn属性
        retrieveAttributes = None
        conn = ldap.initialize(Server)
        # 非常重要
        conn.set_option(ldap.OPT_REFERRALS, 0)
        conn.protocol_version = ldap.VERSION3
        # 这里用户名是域账号的全名例如domain/name
        conn.simple_bind_s(username, password)
        # print 'ldap connect successfully'
        # 调用search方法返回结果id
        ldap_result_id = conn.search(
            baseDN, searchScope, searchFilter, retrieveAttributes
        )
        result_set = []
        while 1:
            result_type, result_data = conn.result(ldap_result_id, 0)
            if result_data == []:
                break
            else:
                if result_type == ldap.RES_SEARCH_ENTRY:
                    result_set.append(result_data)
        Name, Attrs = result_set[0][0]
        if hasattr(Attrs, "has_key") and Attrs.has_key("name"):
            # distinguishedName = Attrs['mail'][0]
            # print "Login Info for user : %s" % distinguishedName
            # print Attrs['mail'][0]
            # print Attrs['name'][0]
            # print Attrs['displayName'][0]
            # print Attrs['memberOf'][0]
            # print Attrs['sAMAccountName'][0]
            # print Attrs['title'][0]
            # print Attrs['department'][0]
            # return distinguishedName
            return Attrs["name"][0]
        else:
            print("in error")
            return None
    except ldap.LDAPError as e:
        print("out error")
        print(e)
        return None


if __name__ == "__main__":
    login_ldap("lijicong", "db1e91061aR")
