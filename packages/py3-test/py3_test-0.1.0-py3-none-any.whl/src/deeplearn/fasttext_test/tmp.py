from collections import Counter

with open("tmp.txt") as f:
    line_list = [line.strip() for line in f.readlines()]
    for k, v in Counter(line_list).most_common():
        print(k, v)
