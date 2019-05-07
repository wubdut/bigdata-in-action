## 项目实践9：开始使用Spark

### step01 Spark Shell
```console
./bin/pyspark
```

```console
textFile = spark.read.text("README.md")

textFile.count()  # Number of rows in this DataFrame
# 126

textFile.first()  # First row in this DataFrame
# Row(value=u'# Apache Spark')

linesWithSpark = textFile.filter(textFile.value.contains("Spark"))
textFile.filter(textFile.value.contains("Spark")).count()  # How many lines contain "Spark"?
# 15

```

### step02 提交Spark任务
```console
./bin/spark-submit examples/src/main/python/wordcount.py
```

### step03 关键代码解析


### step04 使用Dataframe进行Word Count