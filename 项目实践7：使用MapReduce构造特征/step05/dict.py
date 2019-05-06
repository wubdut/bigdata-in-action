#!/usr/bin/env python
"""dict.py"""

import sys,datetime
from filetool import listAllFilesUnderDir, readLines

files = listAllFilesUnderDir('datamap/')
for file in files:
    for line in readLines('datamap/'+file):
        line = line.strip()
        keys = line.split('\t')
        print(keys[0])
