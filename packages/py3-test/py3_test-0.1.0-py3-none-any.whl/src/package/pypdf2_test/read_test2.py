"""
@author: lijc210@163.com
@file: 1.py
@time: 2020/03/26
@desc: 功能描述。
https://blog.csdn.net/xingxtao/article/details/79056341
"""

# encoding:utf-8
from PyPDF2 import PdfFileReader


def getPdfContent(filename):
    pdf = PdfFileReader(open(filename, "rb"))
    # pdf = PdfFileReader(filename)
    content = ""
    for i in range(0, pdf.getNumPages()):
        pageObj = pdf.getPage(i)

        extractedText = pageObj.extractText()
        # print(extractedText.encode("ascii", "ignore"))
        content += extractedText + "\n"
        # print(content.encode("ascii", "ignore"))
    return content


if __name__ == "__main__":
    # readFile = '商家体检报告-上海-金令设计装潢.pdf'
    readFile = "test2.pdf"
    aa = getPdfContent(readFile)
    print(aa)
