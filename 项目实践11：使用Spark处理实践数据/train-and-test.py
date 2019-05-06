from pyspark.sql import SparkSession
from pyspark.sql.functions import split, explode, col
import random
from pyspark.sql import Row

spark = SparkSession.builder.appName("Sample").getOrCreate()
sc = spark.sparkContext

lines = sc.textFile("input/*")
data = lines.map(lambda l: (l.split(","), random.uniform(0, 1)))
train = data.filter(lambda s: s[1] < 0.8).map(lambda s: s[0])
test = data.filter(lambda s: s[1] >= 0.8).map(lambda s: s[0])

spark.stop()