## 项目实践12：使用Spark ML库进行CRT预测

### step01 实现mini-batch gradient descent算法（理解Spark ML对于机器学习的优化原理）

非分布式的机器学习算法在计算迭代梯度时，大量的时间浪费到计算各个维度的梯度方向与大小上，利用spark的分布式计算框架可以将各个维度的梯度计算转化为并行计算，使算法迅速完成梯度计算加快迭代速度。

### step02 利用spark将数据分为训练集和测试集（直接调用Spark ML的库函数）,提交任务：

```console
spark-submit --executor-memory=512M --master yarn-client train-and-test.py
```
### step03 利用线性回归算法进行CTR预估（直接调用Spark ML的库函数）,提交任务：

```console
spark-submit --executor-memory=512M --master yarn-client ctr_prediction.py
```
