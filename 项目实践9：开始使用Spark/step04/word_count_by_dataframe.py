from pyspark.sql import SparkSession  
from pyspark.sql.functions import split, explode, col  
  
spark = SparkSession.builder.appName("wordcount").getOrCreate()  
lines = spark.read.text("README.md")  
  
words = lines.select(explode(split(lines.value, ",")).alias("words"))  
  
words.withColumn('word', explode(split(col('words'), ' ')))\  
    .groupBy('word')\  
    .count()\  
    .sort('count', ascending=False)\  
    .show()
