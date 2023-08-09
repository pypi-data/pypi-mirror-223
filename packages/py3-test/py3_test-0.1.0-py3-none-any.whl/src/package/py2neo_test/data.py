"""
@author: lijc210@163.com
@file: data.py
@time: 2020/03/13
@desc: 功能描述。
"""
import csv

from utils.presto_client import PrestoClient

presto_client = PrestoClient()

# 店铺节点
# sql = "select shop_id,shop_name from dw.ods_weishanghu_wx_shop"
# sql_res = presto_client.query(sql)

# with open("店铺.csv","w") as f:
#     spamwriter = csv.writer(f)
#     # spamwriter.writerows(date_list)
#     for row in sql_res:
#         spamwriter.writerow(row)

# # 品类节点
# sql = "select category_id,name from dw.ods_weishanghu_wx_category"
# sql_res = presto_client.query(sql)
#
# with open("品类.csv","w") as f:
#     spamwriter = csv.writer(f)
#     # spamwriter.writerows(date_list)
#     for row in sql_res:
#         spamwriter.writerow(row)

# # 品牌节点
# sql = "select id,name from dw.ods_weishanghu_brand"
# sql_res = presto_client.query(sql)
#
# with open("品牌.csv","w") as f:
#     spamwriter = csv.writer(f)
#     # spamwriter.writerows(date_list)
#     for row in sql_res:
#         spamwriter.writerow(row)

# 标签节点
# sql = "select id,label_name from dw.ods_weishanghu_label"
# sql_res = presto_client.query(sql)
#
# with open("标签.csv","w") as f:
#     spamwriter = csv.writer(f)
#     # spamwriter.writerows(date_list)
#     for row in sql_res:
#         spamwriter.writerow(row)

# # 店铺-品牌 关系
# sql = """
# select t1.shop_id,t1.shop_name,'品牌' as relation,t3.id,t3.name from dw.ods_weishanghu_wx_shop  t1
# left join dw.ods_weishanghu_shop_brand_mapping t2
# on t1.shop_id = t2.shop_id
# left join dw.ods_weishanghu_brand t3
# on t2.brand_id = t3.id where t3.id is not null
#
# """
# sql_res = presto_client.query(sql)
# with open("店铺对应品牌.csv","w") as f:
#     spamwriter = csv.writer(f)
#     # spamwriter.writerows(date_list)
#     for row in sql_res:
#         spamwriter.writerow(row)

# 店铺-品类 关系
# sql = """
# select t1.shop_id,t1.shop_name,'品类' as relation,t3.category_id,t3.name from dw.ods_weishanghu_wx_shop  t1
# left join dw.ods_weishanghu_wx_category_shop_mapping t2
# on t1.shop_id = t2.shop_id
# left join dw.ods_weishanghu_wx_category t3
# on t2.category_id = t3.category_id where t3.category_id is not null
# """
# sql_res = presto_client.query(sql)
#
# with open("店铺对应品类.csv","w") as f:
#     spamwriter = csv.writer(f)
#     # spamwriter.writerows(date_list)
#     for row in sql_res:
#         spamwriter.writerow(row)

# 店铺-标签 关系
sql = """
select t1.shop_id,t1.shop_name,'标签' as relation,t3.id,t3.label_name from dw.ods_weishanghu_wx_shop  t1
left join dw.ods_weishanghu_shop_label_mapping t2
on t1.shop_id = t2.shop_id
left join dw.ods_weishanghu_label t3
on t2.label_id = t3.id where t3.id is not null
"""
sql_res = presto_client.query(sql)

with open("店铺对应标签.csv", "w") as f:
    spamwriter = csv.writer(f)
    # spamwriter.writerows(date_list)
    for row in sql_res:
        spamwriter.writerow(row)
