## 项目实践8：使用Hive管理实践数据

### step01 创建Hive外部表（External Table）
```console
CREATE EXTERNAL TABLE IF NOT EXISTS  ctr_data (  
    id STRING，  
    click INT，  
    hour STRING，  
    C1 STRING，  
    banner_pos STRING，  
    site_id STRING，  
    site_domain STRING，  
    site_category STRING，  
    app_id STRING，  
    app_domain STRING，  
    app_category STRING，  
    device_id STRING，  
    device_ip STRING，  
    device_model STRING，  
    device_type STRING，  
    device_conn_type STRING，  
    C14 STRING，  
    C15 STRING，  
    C16 STRING，  
    C17 STRING，  
    C18 STRING，  
    C19 STRING，  
    C20 STRING，  
    C21 STRING，  
)  
ROW FORMAT DELIMITED FIELDS TERMINATED BY '，'  
STORED AS TEXTFILE  
LOCATION '/exp/hive/data'; 
```

### step02 使用HQL进行统计
```console
select click, count(*) from ctr_data group by click;
```

### step03 HQL多轮统计
```console
select t.site_id, t.total_click/t.total_show as ctr 
from ( 
  select site_id, sum(click) as total_click, count(*) as total_show 
  from ctr_data 
  group by site_id
) t 
order by ctr limit 10;  
```

