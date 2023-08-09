"""
Created on 2017/6/15 0015
@author: lijc210@163.com
Desc: 功能描述。
"""
import smtplib
import traceback
from email.mime.text import MIMEText


class Mail:
    def __init__(self, mail_to, mail_cc):
        # 发送服务器列表
        self.mail_list = [
            {
                "mail_host": "smtp.163.com",
                "mail_user": "lijcmonitor@163.com",
                "mail_pass": "monitor2016",
                "mail_from": "lijcmonitor@163.com",
            },
            {
                "mail_host": "smtp.aliyun.com",
                "mail_user": "lijcmonitor@aliyun.com",
                "mail_pass": "monitor2016",
                "mail_from": "lijcmonitor@aliyun.com",
            },
            {
                "mail_host": "smtp.sina.com",
                "mail_user": "lijcmonitor@sina.com",
                "mail_pass": "lijcmonitor210",
                "mail_from": "lijcmonitor@sina.com",
            },
        ]
        self.mail_to = mail_to  # 邮件接收者
        self.mail_cc = mail_cc  # 邮件抄送者

    def send(self, subject, content):
        for mail_dict in self.mail_list:
            mail_host = mail_dict["mail_host"]  # 邮箱服务器地址
            mail_user = mail_dict["mail_user"]  # 用户名
            mail_pass = mail_dict["mail_pass"]  # 密码
            mail_from = mail_dict["mail_from"]  # 发送方邮箱地址

            try:
                message = MIMEText(content, "plain", "utf-8")  # 邮件内容设置
                message["Subject"] = subject  # 邮件主题
                message["From"] = mail_from  # 邮件发送人邮箱
                message["Cc"] = ", ".join(self.mail_cc)  # 邮件发送人邮箱
                # 登录并发送邮件
                smtpObj = smtplib.SMTP()
                # 连接到服务器
                smtpObj.connect(mail_host, 25)
                # 登录到服务器
                smtpObj.login(mail_user, mail_pass)
                # 发送
                smtpObj.sendmail(mail_from, self.mail_to, message.as_string())
                # 退出
                smtpObj.quit()
            except Exception:
                print("fail", mail_dict)
                traceback.print_exc()
            else:
                print("success", mail_dict)
                break


if __name__ == "__main__":
    # #发送邮件
    import time

    datetime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    subject = "邮件主题" + str(datetime)
    content = "邮件内容"
    mail_to = ["lijicong1@qeeka.com"]
    mail_cc = ["lijicong1@qeeka.com"]
    mail = Mail(mail_to, mail_cc)
    mail.send(subject, content)
