from pyspark.sql import SparkSession  
from pyspark.sql.functions import split, explode, col  
  
spark = SparkSession.builder.appName("wordcount").getOrCreate()  
datas = spark.read.csv("/home/shizifan/sample", inferSchema=True, header=True)  
datas.show()  
  
datas.printSchema()  
  
datas.columns  
datas.count()  
  
datas.describe('C1').show()  
  
datas.select('site_domain', 'site_id').distinct().show()  
  
datas.filter(datas.click == 1).show()  
datas.filter(datas.click == 1).count()  
  
datas.orderBy('site_domain')  
