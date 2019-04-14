1. 单步调试：
```console
head -300000 ../../data/train | python mapper.py | sort -k1,1 | python reducer.py | sort -k2,2nr | head -n 10
```
2. 运行
```console
sudo -u hdfs hadoop jar /opt/cloudera/parcels/CDH-6.1.0-1.cdh6.1.0.p0.770702/lib/hadoop-mapreduce/hadoop-streaming.jar \
-D map.output.key.field.separator=, \
-D mapred.text.key.partitioner.options=-k8,8 \
-D mapred.reduce.tasks=4 \
-partitioner org.apache.hadoop.mapred.lib.KeyFieldBasedPartitioner \
-input /exp/kaggle/input2/* \
-output /exp/kaggle/output12 \
-mapper mapper.py \
-reducer reducer.py \
-file mapper.py \
-file reducer.py
```