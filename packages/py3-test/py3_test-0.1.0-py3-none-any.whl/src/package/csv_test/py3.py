"""
@Time   : 2018/9/19
@author : lijc210@163.com
@Desc:  : 功能描述。
"""
import csv

date_list = []
with open(r"1.csv") as f:
    reader = csv.reader(f)
    for line in reader:
        date_list.append(line)

with open(r"2.csv", "w", newline="") as csvfile:
    spamwriter = csv.writer(csvfile)
    # spamwriter.writerows(date_list)
    for row in date_list:
        spamwriter.writerow(row)
