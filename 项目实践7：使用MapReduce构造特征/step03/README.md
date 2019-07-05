1. 单步调试：
```console
head -300000 ../../data/train | python mapper.py | sort -k1,1n | python reducer.py
```
2. 运行
```console
hadoop jar /opt/cloudera/parcels/CDH-6.2.0-1.cdh6.2.0.p0.967373/lib/hadoop-mapreduce/hadoop-streaming.jar \
-D map.output.key.field.separator=, \
-D mapred.text.key.partitioner.options=-k3,3 \
-D mapred.reduce.tasks=8 \
-partitioner org.apache.hadoop.mapred.lib.KeyFieldBasedPartitioner \
-input /user/demo/input/* \
-output /user/demo/output \
-mapper mapper.py \
-reducer reducer.py \
-file mapper.py \
-file reducer.py
```
