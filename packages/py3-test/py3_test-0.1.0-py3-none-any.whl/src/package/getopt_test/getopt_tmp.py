"""
@author: lijc210@163.com
@file: getopt_tmp.py
@time: 2019/09/06
@desc: 功能描述。
"""

# !/usr/bin/python
# -*- coding: UTF-8 -*-

import getopt
import sys


def main(argv):
    inputfile = ""
    outputfile = ""
    try:
        opts, args = getopt.getopt(argv, "hi:o:", ["ifile=", "ofile="])
    except getopt.GetoptError:
        print("process_url_path.py -i <inputfile> -o <outputfile>")
        sys.exit(2)
    for opt, arg in opts:
        if opt == "-h":
            print("process_url_path.py -i <inputfile> -o <outputfile>")
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-o", "--ofile"):
            outputfile = arg
    print("输入的文件为：", inputfile)
    print("输出的文件为：", outputfile)


if __name__ == "__main__":
    main(sys.argv[1:])
