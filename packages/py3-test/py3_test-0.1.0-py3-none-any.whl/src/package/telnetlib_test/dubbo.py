"""
@Time   : 2019/4/23
@author : lijc210@163.com
@Desc:  : 功能描述。
"""
import telnetlib

tn = telnetlib.Telnet("172.17.15.93", "20880")
# tn.write(b"invoke com.alibaba.dubbo.demo.DemoService.sayHello(\"world\")\n")
tn.write(b"\n")
tn.write(b"ls\n")
