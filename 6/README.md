## 项目实践6：使用Hbase管理用户数据

在我们的数据中，我们可以看到每次广告展现都是一行数据，如果我们想知道一个站点（site）的历史点击率，我们需要读取一段时间数据进行统计。但是如果历史点击率是一个经常查询的条件，而每次查询都要计算的话则会耗费大量计算资源。因此我们需要一个数据库进行存储，这样只需要一次计算，以后查询就只需要按照key进行检索即可。

### step01

#### 列举数据库中所有表
```console
hbase(main):043:0> list
```

#### 创建表
```console
hbase(main):043:0> create 'table_name', 'cf1', 'cf2'
```
其中的 cf1 和 cf2 为列族名 1，列族名 2，列族需要在见表时确定，列则不需要， Column Family 是 Schema 的一部分，设计时就需要考虑。

#### 删除表
在删除表之前需要使用 disable 命令，让表失效。在修改表结构时，也需要先执行此命令。
```console
hbase(main):043:0> disable "table_name"
```
删除表使用 drop 命令
```console
hbase(main):043:0> drop 'table_name'
```

#### 测试表是否存在
```console
hbase(main):043:0> exists 'table_name'
```
会显示表是否存在：
hbase(main):002:0> exists 'test'
Table test does exist
0 row(s) in 0.2650 seconds
#### 显示表结构
describe 命令查看表结构，显示 HBase 表 schema，以及 column family 设计
```console
hbase(main):043:0> describe 'table_name'
```
#### 使表有效
enable 命令，和 disable 命令对应
```console
hbase(main):043:0> enable 'table_name'
```
#### 修改表结构
alter 修改表的结构，新增列族，删除列族。在修改之前要先 disable ，修改完成后再 enable
新增列族
```console
hbase(main):043:0> alter 'table_name', '列族'
```
删除列族
```console
hbase(main):043:0> alter 'table_name', {name=>'列族', METHOD=>'delete'}
```

#### 增加记录
put 命令

插入数据，对于同一个 rowkey，如果执行两次 put，则认为是更新操作
```console
hbase(main):043:0> put 'table_name', 'rowkey', '列族名 1: 列名 1', 'value'
hbase(main):043:0> put 't1', 'r1', 'c1', 'value', ts1 
```
一般情况下 ts1（时间戳） 可以省略， Column 可以动态扩展，每行可以有不同的 Column。
#### 查询表行数
计算表的行数，count 一般比较耗时，使用
```console
hbase(main):043:0> count 'table_name'
```
#### 查询所有 rowkey
```console
hbase(main):043:0> count 'table_name', { INTERVAL => 1 }
```
#### 获取指定 rowkey 的指定列族所有的数据
```console
hbase(main):043:0> get 'table_name', 'rowkey', '列族名'
```
#### 获取指定 rowkey 的所有数据
```console
hbase(main):043:0> get 'table_name', 'rowkey'
```
#### 获取指定时间戳的数据
```console
hbase(main):043:0> get 'table_name', 'rowkey', {COLUMN=>'列族名：列', TIMESTAMP=>1373737746997}
```
#### 删除指定 rowkey 的指定列族的列名数据
```console
hbase(main):043:0> delete 'table_name', 'rowkey', '列族名：列名'
```
#### 删除指定 rowkey 指定列族的数据
```console
hbase(main):043:0> delete 'table_name', 'rowkey', '列族名'
```
#### 删除整行数据
```console
hbase(main):043:0> deleteall 'table_name', ’rowkey'
```
#### 全表扫描
scan
```console
hbase(main):043:0> scan 'test', {VERSIONS => 12}
ROW                         COLUMN+CELL
 rowkey1                    column=cf:a, timestamp=1487295285291, value=value 3
 rowkey1                    column=cf:a, timestamp=1487294839168, value=value 2
 rowkey1                    column=cf:a, timestamp=1487294704187, value=value 1
```
#### hbase shell 脚本
shell 命令，把所有的 hbase shell 命令写到一个文件内，类似与 Linux shell 脚本顺序执行所有命令，可以使用如下方法执行。
```console
hbase(main):043:0> hbase shell test.hbaseshell
```

### step02 使用Python进行Hbase数据读写
#### 通过行键获取数据
```python
import hbase  

zk = '127.0.0.1:2181'  

if __name__ == '__main__':  
    with hbase.ConnectionPool(zk).connect() as conn:  
        table = conn['mytest']['videos']  
        row = table.get('00001')  
        print(row)  
    exit() 
```

#### 扫描表
```python
import hbase  

zk = '127.0.0.1:2181'

if __name__ == '__main__':  
    with hbase.ConnectionPool(zk).connect() as conn:  
        table = conn['mytest']['videos']  
        for row in table.scan():  
            print(row)  
    exit()
```

#### 写入一条记录
```python
import hbase  

zk = '127.0.0.1:2181' 
  
if __name__ == '__main__':  
    with hbase.ConnectionPool(zk).connect() as conn:  
        table = conn['mytest']['videos']  
        table.put(hbase.Row(  
            '0001', {  
                'cf:name': b'Lily',  
                'cf:age': b'20'  
           }  
        ))
    exit()
```

### step03 Hbase保存用户数据
将app_id进行编号，并存入hbase。用于后期对特征的正则化和归一化。
