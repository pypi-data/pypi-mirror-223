"""
@Time   : 2018/9/5
@author : lijc210@163.com
@Desc:  : 函数异常，发送通知
"""
import time
import traceback

from mail import Mail
from weixin import Weixin


def try_except(fun):
    def notice(*args, **kwargs):
        try:
            fun(*args, **kwargs)
        except Exception:
            traceback.print_exc()

            fun_name = fun.__name__
            error_content = traceback.format_exc()
            datetime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            subject = fun_name + str(datetime) + "出错"
            content = error_content
            # 邮件通知
            mail_to = ["lijicong1@qeeka.com", "henry.xiao@qeeka.com"]
            mail_cc = ["lijicong1@qeeka.com", "henry.xiao@qeeka.com"]
            mail = Mail(mail_to, mail_cc)
            mail.send(subject, content)
            # 微信通知
            weixin = Weixin()
            weixin.send(agentid=1000012, text=subject)

    return notice
