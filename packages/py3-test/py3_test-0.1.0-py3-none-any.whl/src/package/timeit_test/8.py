"""
@author: lijc210@163.com
@file: 8.py
@time: 2019/09/09
@desc: 功能描述。
"""
import timeit

row = {
    b"info:\xe4\xba\x94\xe9\x87\x91\xe5\xb7\xa5\xe5\x85\xb7": b"0.0592",
    b"info:\xe5\x8d\xa7\xe5\xae\xa4": b"0.0598",
    b"info:\xe5\x9c\xb0\xe9\x9d\xa2": b"0.0795",
    b"info:\xe5\xa2\x99\xe5\x9c\xb0\xe9\x9d\xa2": b"0.0592",
    b"info:\xe5\xa4\xa7\xe6\x88\xb7\xe5\x9e\x8b": b"0.0592",
    b"info:\xe5\xae\xa4\xe5\xa4\x96\xe5\x9b\xad\xe8\x89\xba": b"0.1387",
    b"info:\xe6\xb0\xb4\xe7\x94\xb5\xe9\x98\xb6\xe6\xae\xb5": b"0.0795",
    b"info:\xe6\xb2\xb9\xe6\xbc\x86\xe9\x98\xb6\xe6\xae\xb5": b"0.0795",
    b"info:\xe8\xa3\x85\xe4\xbf\xae\xe5\x85\xac\xe5\x8f\xb8": b"0.1183",
    b"info:\xe8\xa3\x85\xe4\xbf\xae\xe8\x89\xb2\xe8\xb0\x83": b"0.1183",
    b"info:\xe8\xbf\x87\xe9\x81\x93": b"0.093",
    b"info:\xe9\x98\x81\xe6\xa5\xbc": b"0.0591",
    b"info:\xe9\x9d\x92\xe5\xb9\xb4": b"0.0399",
    b"info:\xe9\xbd\x90\xe5\xae\xb6\xe7\x94\x9f\xe6\xb4\xbb\xe9\xa6\x86": b"0.1183",
    b"info:avg_log": b"19.823529411764707",
    b"info:avg_num": b"1.392156862745098",
    b"info:layout_counts": b"6",
    b"info:log_days": b"51",
    b"info:luntan_counts": b"7",
    b"info:max_day": b"31",
    b"info:news_counts": b"34",
    b"info:note_counts": b"7",
    b"info:pic_counts": b"6",
    b"info:queans_counts": b"1",
    b"info:question_counts": b"1",
    b"info:special_counts": b"1",
    b"info:text_counts": b"34",
    b"info:udid": b"5008C251-F4BB-42BB-82C6-A7DAF9E031BE",
}


def a():
    {k.decode().replace("info:", ""): v.decode() for k, v in row.items()}
    # print(d)


def b():
    {k.decode()[5:]: v.decode() for k, v in row.items()}
    # print(d)


a()
b()

print(timeit.timeit(stmt=a, number=10000))
print(timeit.timeit(stmt=b, number=10000))
