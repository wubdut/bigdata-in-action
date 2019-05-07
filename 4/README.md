## 项目实践4： 通过Kafka进行数据处理
广告系统产生大量线上展示数据，如果数据直接写入HDFS，Hadoop Session无法承受，而且会严重影响Hadoop性能。因此系统会通过消息中间件作为缓存。本次项目大家需要通过python实现Kafka Producer和Kafka Consumer。
本实践中，我们模拟一个简单的广告业务数据的收集与处理系统。

### step01 Kafka管理
#### 启动服务
Kafka使用ZooKeeper进行配置管理，因此启动Kafka Server之前我们需要先启动Zookeeper Server。
```console
demo@bigdata-in-action:~$bin/zookeeper-server-start.sh config/zookeeper.properties
```
#### 创建Topic
使用Kafka的第一件事情就是创建一个Topic，我们使用如下命令创建一个名字为test的topic。
```console
demo@bigdata-in-action:~$bin/kafka-topics.sh --create --zookeeper localhost:2181 \
--replication-factor 1 --partitions 1 --topic test
```
输出：
```console
Created topic "test".
```
之后我们可以通过下面的命令查看我们的Topic是否已经成功创建
```console
demo@bigdata-in-action:~$bin/kafka-topics.sh --list --zookeeper localhost:2181
```
输出：
```console
test
```
#### 发送数据和消费数据
有了Topic之后，我们就可以使用一个简单的脚本向Kafka的Topic中写入数据，下面的命令启动了一个生产者，等待用户输入。
```console
demo@bigdata-in-action:~$bin/kafka-console-producer.sh --broker-list localhost:9092 --topic test
```
输入：
```console
This is a message
This is another message
```
在写入数据后，我们可以启动一个消费者从Topic中从头读取数据，命令如下：
```console
demo@bigdata-in-action:~$bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic test --from-beginning
```
输出：
```console
This is a message
This is another message
```

### step02实现生产者
生产者从文本文件Train中读取数据，然后写入到Kafka的Topic中，相当于业务系统源源不断产出数据写入到Kafka。

### step03 实现消费者
消费者负责从Kafka的Topic中读取数据，然后进行处理。在广告系统中，该处理过程会直接通过Hadoop任务把数据保存到大数据文件系统。但本过程我们先把数据进行切分写入到本地文件，等到学习完大数据文件系统之后，再把数据导入进去。m
