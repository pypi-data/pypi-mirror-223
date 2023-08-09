"""
@Time   : 2018/9/19
@author : lijc210@163.com
@Desc:  : 功能描述。
"""
import os
import csv


def get_file_path_list(rootdir):
    list = os.listdir(rootdir)  # 列出文件夹下所有的目录与文件
    file_path_list = []
    for i in range(0, len(list)):
        path = os.path.join(rootdir, list[i])
        if os.path.isfile(path):
            file_path_list.append(path)
    return file_path_list


if __name__ == "__main__":
    date_list = []
    file_path_list = get_file_path_list("/mnt/c/Users/lijicong/Desktop")
    i = 0
    for file_path in file_path_list:
        if "厦门市海洋发展局_李继聪" in file_path and "csv" in file_path:
            i += 1
            print(file_path)

            with open(file_path) as f:
                reader = csv.reader(f)
                if i == 1:
                    for line in reader:
                        date_list.append(line)
                        # break
                else:
                    for n, line in enumerate(reader):
                        if n != 0:
                            date_list.append(line)
                            # break

    with open(r"/mnt/c/Users/lijicong/Desktop/all.csv", "w") as csvfile:
        spamwriter = csv.writer(csvfile)
        spamwriter.writerows(date_list)
