"""
@author: lijc210@163.com
@file: 4.py
@time: 2019/09/10
@desc: 功能描述。
spark.executor-core 物理核数
spark.num-executors 每个物理cpu使用的核数
实际executors = spark.executor-core * spark.num-executors
"""
from pyspark import SparkConf, SparkContext, SQLContext
from pyspark.sql import SparkSession

conf = (
    SparkConf()
    .setMaster("spark://10.10.23.31:7077")
    .set("spark.executor.memory", "1g")
    .set("spark.num-executors", "2")
    .set("spark.driver-memory", "2g")
    .set("spark.executor-cores", "2")
    .set("spark.network.timeout", "10000001")
    .set("spark.executor.heartbeatInterval", "10000000")
    .setAppName("rec_total")
    .set("spark.ui.showConsoleProgress", "false")
)

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
