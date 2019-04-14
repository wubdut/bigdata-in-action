1. 单步调试：
```console
head -300000 ../../data/train | python mapper.py | sort -k1,1 | python reducer.py | sort -k2,2nr | head -n 10
```
2. 运行
```console
sudo -u hdfs hadoop jar /opt/cloudera/parcels/CDH-6.1.0-1.cdh6.1.0.p0.770702/lib/hadoop-mapreduce/hadoop-streaming.jar \
-files mapper.py,reducer.py \
-mapper mapper.py \
-reducer reducer.py \
-input /exp/kaggle/input/* -output /exp/kaggle/output
```