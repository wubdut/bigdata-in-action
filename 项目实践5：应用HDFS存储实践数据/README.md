## 项目实践5：应用HDFS存储实践数据

### step01 理解分布式文件系统
为了帮助大家理解分布式系统如何工作，请大家完成（查看）下面的python程序

1)  创建一个Data目录，并按照0 ~ 9 的顺序创建10个目录

2)  该程序需要把1W行数据存储在这10个目录里，但是每个目录下最多只能存储2000行数据。

3)  完成步骤2之后，程序需要接受一个0~9999的数字，返回之前该数字所对应的那行数据。


### step02 理解数据冗余
在实验1的基础上，我多增加一个步骤，实验变为：

1)  创建一个data目录，并按照0 ~ 9 的顺序创建10个目录

2)  该程序需要把1W行数据存储在这10个目录里，但是每个目录下最多只能存储2000行数据。

3)  我选择1~9任意一个数字，然后删掉你的目录

4)  程序需要接受一个0~9999的数字，返回之前该数字所对应的那行数据。

### step03 使用HDFS

HDFS Shell提供了HDFS最基础的操作功能，包括查看目录，创建和删除文件，移动和复制文件等等。

#### 切换到hdfs用户
```console
demo@bigdata-in-action:$ su - hdfs
```
#### 创建目录：mkdir
```console
demo@bigdata-in-action:$ hadoop fs -mkdir /user/hadoop/input
```
#### 上传实验数据到该目录
```console
demo@bigdata-in-action:$ hadoop fs -copyFromLocal ./part-0000* /user/hadoop/input
```
#### 查看文件并统计行数
```console
demo@bigdata-in-action:$ hadoop fs -cat /user/hadoop/exp/input/part-00000 | less
demo@bigdata-in-action:$ hadoop fs -cat /user/hadoop/exp/input/part-00000 | wc -l
```

### step04 数据拷贝测试
#### hadoop fs -cp
```console
demo@bigdata-in-action:$ hadoop fs -mkdir /user/hadoop/exp/test1
demo@bigdata-in-action:$ hadoop fs -cp /user/hadoop/exp/input/part-*  /user/hadoop/exp/test1
```
#### hadoop distcp
```console
demo@bigdata-in-action:$ hadoop fs -mkdir /user/hadoop/exp/test2
demo@bigdata-in-action:$ hadoop distcp /user/hadoop/exp/input /user/hadoop/exp/test2
```
distcp是作为一个MapReduce作业来实现的，该复制作业是通过集群中并行运行的map来完成，这里没有reduce过程。每个文件通过一个map进行复制，并且distcp试图为每一个map分配大致相等的数据来执行，即把文件划分为大致相等的块。

## 学习资料

HDFS SHELL查询手册：https://hadoop.apache.org/docs/r2.4.1/hadoop-project-dist/hadoop-common/FileSystemShell.html

HDFS源码：https://github.com/apache/hadoop-hdfs

DistCp手册：https://hadoop.apache.org/docs/current/hadoop-distcp/DistCp.html

## 常见问题：
#### 文件权限问题
HDFS的文件权限与Linux文件权限基本一致，因此也会出现在操作文件时出现Permision Denied的问题。
