"""
@author: lijc210@163.com
@file: scan_url.py
@time: 2019/08/27
@desc: 功能描述。
"""
from collections import Counter, defaultdict

default_dict = defaultdict(dict)
url_title_dict = {}

with open("tag.txt", encoding="utf-8") as f:
    for _i, line in enumerate(f.readlines()):
        # print(i)
        line_list = line.strip().split()
        tag = line_list[0]
        url = line_list[1]
        if url == "http://www.idp.cn/suzhou/aozhou/shuoshi/132858.html":
            score = line_list[2]
            title = line_list[3]
            default_dict[url][tag] = score

###### 统计二

all_tag_list = []
for url, adict in default_dict.items():
    print(url)
    new_dict = {tag: float(score) for tag, score in adict.items()}
    tmp_counter = Counter(new_dict)
    print(tmp_counter.most_common())
    tmp_list = [tag for tag, score in tmp_counter.most_common(10)]
    all_tag_list.extend(tmp_list)

all_tag_counter = Counter(all_tag_list)
print(all_tag_counter.most_common(100))
