#!/usr/bin/env python
"""
run.py
"""

f = open('../../data/train','r')

res01 = 0       # for 1)
res02 = dict()  # for 2)
res03 = dict()  # for 3)

line_tmp = f.readline()

while True:
    line = f.readline()
    if not line:
        break
        
    res01 = res01 + 1
    
    line = line.strip()
    keys = line.split(',')
    
    if res02.get(keys[7]):
        res02[keys[7]] = res02[keys[7]] + 1
    else:
        res02[keys[7]] = 1
        
    if res03.get(keys[7] + ',' + keys[14]):
        res03[keys[7] + ',' + keys[14]] = res03[keys[7] + ',' + keys[14]] + 1
    else:
        res03[keys[7] + ',' + keys[14]] = 1
    
f.close()

print(res01)
print(res02)
print(res03)