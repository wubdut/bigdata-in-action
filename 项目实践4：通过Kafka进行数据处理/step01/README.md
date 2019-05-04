#### 启动服务
Kafka使用ZooKeeper进行配置管理，因此启动Kafka Server之前我们需要先启动Zookeeper Server。命令如下：
> bin/zookeeper-server-start.sh config/zookeeper.properties
[2019-03-12 15:11:30,836] INFO Reading configuration from: config/zookeeper.properties (org.apache.zookeeper.server.quorum.QuorumPeerConfig)

如果启动后出现java.net.BindException: Address already in use这样的错误，说明zookeeper想要使用的2181端口已经被占用。这时我们可以通过如下命令查看2181端口被哪个进程占用：
> lsof -i:2181
COMMAND   PID      USER   FD   TYPE    DEVICE SIZE/OFF NODE NAME
java    17177 zookeeper   41u  IPv4  43551758      0t0  TCP *:eforward (LISTEN)

从上面的信息我们可以看到我们已经有一个Zookeeper在运行了，这是因为我们启动的Hadoop也使用了Zookeeper，这样我们就不需要再次启动Zookeeper了。但是如果该端口号不是被zookeeper占用，我们就需要考虑是kill掉占用的进程释放端口号，还是通过修改配置让zookeeper服务使用其他端口号。Zookeeper的端口号配置在config/zookeeper.properties中，设置方法在行“clientPort=2181”。
确认了Zookeeper正常启动后，我们开始启动Kafka Server
> bin/kafka-server-start.sh config/server.properties
[2019-03-12 15:13:19,621] INFO Registered kafka:type=kafka.Log4jController MBean (kafka.utils.Log4jControllerRegistration$)

需要注意的是，如果我们在启动Zookeeper的时候修改了端口号，那么对应的也需要在Kafka Server的配置文件config/server.properties中进行修改，设置方法在行“zookeeper.connect=localhost:2181”
#### 创建Topic
使用Kafka的第一件事情就是创建一个Topic，我们使用如下命令创建一个名字为test的topic。
> bin/kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 1 --partitions 1 --topic test
Created topic "test".
之后我们可以通过下面的命令查看我们的Topic是否已经成功创建
> bin/kafka-topics.sh --list --zookeeper localhost:2181
test
发送数据和消费数据
有了Topic之后，我们就可以使用一个简单的脚本向Kafka的Topic中写入数据，下面的命令启动了一个生产者，等待用户输入。
> bin/kafka-console-producer.sh --broker-list localhost:9092 --topic test
输入数据：
This is a message
This is another message
在写入数据后，我们可以启动一个消费者从Topic中从头读取数据，命令如下：
> bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic test --from-beginning
This is a message
This is another message
