#!/usr/bin/env python
"""reducer.py"""

from operator import itemgetter
import sys

dict = {
    't0': 0,
    't1': 1,
    'p1': 2,
    'p7': 3
}

current_key = None
current_value = ['0', '0', '0', '0']
person = None
cli = None
attr = None

# input comes from STDIN
for line in sys.stdin:
    # remove leading and trailing whitespace
    line = line.strip()

    # parse the input we got from mapper.py
    person, cli = line.split('\t', 1)
    key = person[:-3]
    attr = person[-2:]
    # this IF-switch only works because Hadoop sorts map output
    # by key (here: word) before it is passed to the reducer
    if current_key == key:
        current_value[dict[attr]] = cli
    else:
        if current_key:
            # write result to STDOUT
            print ('%s,%s' % (current_key, ','.join(current_value)))
        current_key = key
        current_value[dict[attr]] = cli

# do not forget to output the last word if needed!
if current_key == key:
    print ('%s,%s' % (current_key, ','.join(current_value)))
