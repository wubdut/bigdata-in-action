1. 单步调试：
head -n 30000 ../../data/train | python3 mapper.py | python3 reducer.py

2. 第一轮mapreduce：

sudo -u hdfs hadoop jar /opt/cloudera/parcels/CDH-6.1.0-1.cdh6.1.0.p0.770702/lib/hadoop-mapreduce/hadoop-streaming.jar \
-files mapper.py,reducer.py \
-mapper mapper.py \
-reducer reducer.py \
-input /exp/kaggle/input/* -output /exp/kaggle/output3

3. 单步调试：
hdfs dfs -tail /exp/kaggle/output3/part-00000 | python3 mapper2.py | python3 reducer2.py

4. 第二轮mapreduce：

sudo -u hdfs hadoop jar /opt/cloudera/parcels/CDH-6.1.0-1.cdh6.1.0.p0.770702/lib/hadoop-mapreduce/hadoop-streaming.jar \
-files mapper2.py,reducer2.py \
-mapper mapper2.py \
-reducer reducer2.py \
-input /exp/kaggle/output3/* -output /exp/kaggle/output4