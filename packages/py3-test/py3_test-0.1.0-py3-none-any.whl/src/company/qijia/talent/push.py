"""
@Time   : 2018/9/25
@author : lijc210@163.com
@Desc:  : 功能描述。
"""

with open(r"tmp\push.log.2018-09-25", "w") as fw:
    with open("push.log.2018-09-25") as fr:
        for line in fr.readlines():
            line_list = line.strip().split("\001")
            if len(line_list) != 1:
                push_id = line_list[2]
                print(push_id)
                line_list.pop(2)
                line_list.append(push_id)
                print(line_list)
                fw.write("\001".join(line_list) + "\n")
