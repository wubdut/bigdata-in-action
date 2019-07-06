#!/usr/bin/env python
import sys

dict = {}

for line in sys.stdin:
    line = line.strip()
    key,val = line.split('\t', 1)

    try:
        val = int(val)
    except ValueError:
        continue

    dict[key] = val

res = sorted(dict.items(), key=lambda d: d[1], reverse=True)
for i in range(10):
    print('%s\t%s' % (res[i][0], res[i][1]))
