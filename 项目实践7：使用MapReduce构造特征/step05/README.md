1. 单步调试：
```console
head -n 30000 ../../data/train | python3 mapper.py | python3 reducer.py
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
-files mapper2.py,reducer2.py \
-mapper mapper2.py \
-reducer reducer2.py \
-input /user/demo/output-feature-tmp/* -output /user/demo/output-feature-csv
```
