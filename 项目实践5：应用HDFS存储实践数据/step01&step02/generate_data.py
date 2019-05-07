#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 2019年3月3日
第二章 实验一

@author: wubin
'''

from filetool import delAllFilesUnderDir, getWriteOneLineHandle, writeOneLine,makeDir

# 定义静态变量 #
DATA_DIR = 'data/'
DATA_DIR_REPLICATION = 'data_rep/'
MAX_LINES_PER_FILE = 2000
# ----END---- #

# 创建文件夹 #
makeDir(DATA_DIR)
makeDir(DATA_DIR_REPLICATION)
# ----END---- #

# 清空数据目录 #
delAllFilesUnderDir(DATA_DIR)
delAllFilesUnderDir(DATA_DIR_REPLICATION)
# ----END---- #


# 向文件写入数据 #
for index in range(10000):
    currentFile = index // MAX_LINES_PER_FILE
    dataHandle = getWriteOneLineHandle(DATA_DIR+str(currentFile))
    dataHandleRep = getWriteOneLineHandle(DATA_DIR_REPLICATION+str(currentFile))
    # 写原本
    writeOneLine(dataHandle, str(index)+' context')
    # 写副本
    writeOneLine(dataHandleRep, str(index)+' context')
    
dataHandle.close()
dataHandleRep.close()
# -----END---- #

print('结束')