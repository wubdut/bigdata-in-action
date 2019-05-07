1. 预处理单步调试：
```console
head -n 30000 ../../data/train | python3 mapper_pre.py | sort -k1,1 | python3 reducer_pre.py
```
2. 预处理mapreduce：
```console
mapred streaming \
-files mapper_pre.py,reducer_pre.py \
-mapper mapper_pre.py \
-reducer reducer_pre.py \
-input /user/demo/input/* -output /user/demo/output-feature-map
```

3. 预处理拷贝：
```console
hadoop fs -copyToLocal /user/demo/output-feature-map datamap
rm datamap/_SUCCESS
```

4. 生成字典：
```console
python3 dict.py > dict
```

1. 单步调试：
```console
head -n 30000 ../../data/train | python3 mapper.py | sort -k1,1 | python3 reducer.py
```
2. 第一轮mapreduce：
```console
mapred streaming \
-files mapper.py,reducer.py \
-mapper mapper.py \
-reducer reducer.py \
-input /user/demo/input/* -output /user/demo/output-feature-tmp
```

3. 单步调试：
```console
hadoop fs -tail /user/demo/output-feature-tmp/part-00000 | python3 mapper2.py | python3 reducer2.py
```

4. 第二轮mapreduce：
```console
mapred streaming \
-files mapper2.py,reducer2.py,dict \
-mapper mapper2.py \
-reducer reducer2.py \
-input /user/demo/output-feature-tmp/* -output /user/demo/output-feature-csv
```
