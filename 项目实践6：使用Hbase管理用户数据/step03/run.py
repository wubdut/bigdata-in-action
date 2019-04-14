#!/usr/bin/env python
"""
run.py
"""
import hbase

zk = '127.0.0.1:2181'

f = open('../../data/train','r')
st = set()
dt = dict()
while True:
    line = f.readline()
    if not line:
        break
    line = line.strip()
    keys = line.split(',')
    st.add(keys[8])
f.close()

cnt = 0

for key in st:
    dt['map:'+key] = str(cnt).encode('utf-8')
    cnt = cnt + 1

# print(dt)

with hbase.ConnectionPool(zk).connect() as conn:
    table = conn['kaggle']['key']
    table.put(hbase.Row(
        'app_id', dt
    ))
exit()