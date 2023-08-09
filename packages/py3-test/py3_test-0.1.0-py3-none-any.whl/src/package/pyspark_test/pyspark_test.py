"""
@author: lijc210@163.com
@file: 4.py
@time: 2019/09/10
@desc: 功能描述。
"""
from pyspark import SparkConf, SparkContext, SQLContext
from pyspark.sql import SparkSession

# 正式执行
# conf = SparkConf()\
#     .setMaster("local[*]") \
#     .set("spark.executor.memory", '2g') \
#     .set("spark.num-executors", '30') \
#     .set("spark.driver-memory", '10g') \
#     .set("spark.executor-cores", '2') \
#     .set("spark.network.timeout", "10000001") \
#     .set("spark.executor.heartbeatInterval", "10000000") \
#     .setAppName("rec_total") \
#     .set("spark.ui.showConsoleProgress", "false")
conf = SparkConf().setMaster("local[*]")
sc = SparkContext(conf=conf)
sqlContext = SQLContext(sc)
spark = SparkSession(sc)

myData = sc.parallelize([(1, 2), (3, 4), (5, 6), (7, 8), (9, 10)])
print(myData.collect())

Employee = spark.createDataFrame(
    [
        ("1", "Joe", "70000", "1"),
        ("2", "Henry", "80000", "2"),
        ("3", "Sam", "60000", "2"),
        ("4", "Max", "90000", "1"),
    ],
    ["Id", "Name", "Sallary", "DepartmentId"],
)

print(Employee.show())

if __name__ == "__main__":
    pass
