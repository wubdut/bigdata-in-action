## 项目实践7：使用MapReduce构造特征

### step01 WordCount
datafile目录中有许多本小说文本，统计出现次数最高的10个单词：

1)  通过多个进程进行统计，限定每个进程最多读取5M的数据；

2)  尝试先将首字母相同的单词写入相同文件，然后对每个文件单独进行统计。（模拟shuffle过程，使得学生更好理解shuffle在map后以及reduce前所起的作用）

### step02 特征统计
统计train文件中的domain的分布。

1)  通过单步调试测试代码；

2)  通过hadoop stream完成统计。


### step03 Reduce过程的负载均衡：
1)  统计train中总的点击次数和未点击次数，并查看reducer的工作情况。

2)  由于现在的计算机都是多核的，且计算框架也趋向分布式。思考如何增加reducer的数目，提高运算速率。（提示：修改hadoop streaming的参数）

### step04 二次排序：
通过上一步学习到的partition配置，统计每个site_category下面site_domain的分布。

### step05 特征提取：
device_id,app_id,device_type,app_domain,hour,t0,t1,p1,p7
其中，t0：当天未点击次数；t1：当天点击次数；p1：前一天点击次数；p7：前7天点击次数。
