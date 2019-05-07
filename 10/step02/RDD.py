# coding:utf-8

import partition as pt
import os
import copy
import sys
from queue import Queue


class RDD:
    MAP = "map"
    FILTER = "filter"
    REDUCE = "reduce"

    def __init__(self, path, tmp_dir="tmp/"):
        print('create RDD')
        self.path = path
        self.tmp_dir = tmp_dir
        self.partitions = []
        self.lazy = []

    def load(self):
        ls = os.listdir(self.tmp_dir)
        for name_file in ls:
            os.remove(os.path.join(self.tmp_dir, name_file))
        reduce_partitions = []
        lines = []
        file_data = open(self.path, 'r')
        for line in file_data:
            lines.append(line.strip())
            if sys.getsizeof(lines) > 1024 * 1024 * 4:
                reduce_partitions.extend(pt.Partition(lines, copy.copy(self.lazy)).action())
                lines = []
        file_data.close()
        if lines:
            reduce_partitions.extend(pt.Partition(lines, copy.copy(self.lazy)).action())
        return reduce_partitions

    def map(self, func):
        self.lazy.append((self.MAP, func))
        return self

    def filter(self, func):
        self.lazy.append((self.FILTER, func))
        return self

    def reduce(self, value, func):
        reduce_partitions = self.load()
        for reduce_partition in reduce_partitions:
            value = reduce_partition.reduce(value, func)
        return value


def map_func(feature):
    return feature.split(',')[4]


def filter_func(value):
    return value is '0'


def count(value_a, value_b):
    return int(value_a) + 1


rdd = RDD("../../data1")
print("垃圾广告数量为：%s\n" % rdd.map(map_func).filter(filter_func).reduce(0, count))
