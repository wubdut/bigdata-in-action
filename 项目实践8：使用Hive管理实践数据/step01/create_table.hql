CREATE EXTERNAL TABLE IF NOT EXISTS  ctr_data (
    id STRING,
    click INT,
    hour STRING,
    C1 STRING,
    banner_pos STRING,
    site_id STRING,
    site_domain STRING,
    site_category STRING,
    app_id STRING,
    app_domain STRING,
    app_category STRING,
    device_id STRING,
    device_ip STRING,
    device_model STRING,
    device_type STRING,
    device_conn_type STRING,
    C14 STRING,
    C15 STRING,
    C16 STRING,
    C17 STRING,
    C18 STRING,
    C19 STRING,
    C20 STRING,
    C21 STRING
)
ROW FORMAT DELIMITED FIELDS TERMINATED BY ','
STORED AS TEXTFILE
LOCATION '/user/demo/upload/';
