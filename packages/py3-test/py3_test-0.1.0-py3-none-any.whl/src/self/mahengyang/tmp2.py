"""
@author: lijc210@163.com
@file: tmp2.py
@time: 2019/10/22
@desc: 功能描述。
"""
with open("tag1111.txt", "w", encoding="utf-8") as fw:
    with open("tag.txt", encoding="utf-8") as f:
        for line in f.readlines():
            line_list = line.strip().split("\t")
            if line_list[1] in {
                "http://wap.idp.cn/yingguo/remenyuanxiao/129211.html",
                "http://wap.idp.cn/yingguo/remenyuanxiao/129547.html",
                "http://wap.idp.cn/meiguo/shenqingtiaojian/117645.html",
                "http://wap.idp.cn/yingguo/remenzhuanye/129548.html",
                "http://www.idp.cn/guangzhou/jiangzuomianshi/2140.html",
                "http://www.idp.cn/yingguo/zexiaozhidao-WY2002/83995.html",
                "http://www.idp.cn/shanghai/jiangzuomianshi/33617.html",
                "http://www.idp.cn/shenzhen/jiangzuomianshi/2141.html",
            }:
                print("aaaaaaaaaaa")
                continue
            fw.write(line)
