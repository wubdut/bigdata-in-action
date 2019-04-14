#!/usr/bin/env python
"""
run.py
"""
from kafka import KafkaProducer  

data_path = '/data/bigdata-in-action/train'  

producer = KafkaProducer(bootstrap_servers='localhost:9092')  

line_num = 0  
for line in open(data_path):  
    line_num += 1  
    if line_num == 1:  
        continue  
  
    if line_num == 1000:  
        producer.flush()  
  
    producer.send('test', line.strip().encode('utf8')) 
