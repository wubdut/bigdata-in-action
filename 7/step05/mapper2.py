#!/usr/bin/env python
"""mapper.py"""

import sys,datetime

device_id_cnt = 0
device_id = {}
app_id_cnt = 0
app_id = {}
app_domain_cnt = 0
app_domain = {}

f = open('dict',"r", encoding='utf-8', errors = 'ignore')
data = f.readlines()
f.close()

for item in data:
    item = item.strip()
    types= item.split(':')
    if types[0] == 'device_id':
        device_id[types[1]] = str(device_id_cnt)
        device_id_cnt = device_id_cnt + 1
    elif types[0] == 'app_id':
        app_id[types[1]] = str(app_id_cnt)
        app_id_cnt = app_id_cnt + 1
    elif types[0] == 'app_domain':
        app_domain[types[1]] = str(app_domain_cnt)
        app_domain_cnt = app_domain_cnt + 1

for line in sys.stdin:
    line = line.strip()
    keys = line.split('\t')
    tmp = keys[0]
    items = tmp.split(',')
    if items[0] in device_id:
        items[0] = device_id[items[0]]
    if items[1] in app_id:
        items[1] = app_id[items[1]]
    if items[3] in app_domain:
        items[3] = app_domain[items[3]]
    print ('%s\t%s' % (','.join(items), keys[1]))
