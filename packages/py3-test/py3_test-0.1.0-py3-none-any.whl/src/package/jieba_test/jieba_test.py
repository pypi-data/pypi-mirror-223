"""
Created on 2015/12/28
@author: lijc210@163.com

"""
# import sys
#
# sys.setdefaultencoding('utf8')

import jieba

content = "家庭桑拿室"
print(",".join(jieba.cut(content)))
# 家庭,桑拿室
print(",".join(jieba.cut_for_search(content)))
# 家庭,桑拿,桑拿室
