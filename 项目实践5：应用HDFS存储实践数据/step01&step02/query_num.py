#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 2019年1月5日
第二章 实验一

@author: wubin
'''

from filetool import getLineInFile, fileExist

# 定义静态变量 #
DATA_DIR = 'data/'
DATA_DIR_REPLICATION = 'data_rep/'
MAX_LINES_PER_FILE = 2000
# ----END---- #


# 按行查询 #
rowNum = 1001
currentFile = rowNum // MAX_LINES_PER_FILE
currentLineInCurrentFile = rowNum % MAX_LINES_PER_FILE

if fileExist(DATA_DIR+str(currentFile)):
    print(getLineInFile(DATA_DIR+str(currentFile), currentLineInCurrentFile))
else:
    print(getLineInFile(DATA_DIR_REPLICATION+str(currentFile), currentLineInCurrentFile))
# -----END---- #

print('结束')