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

    def clear(self):
        self.partitions = []

    def load(self):
        ls = os.listdir(self.tmp_dir)
        for name_file in ls:
            os.remove(os.path.join(self.tmp_dir, name_file))
        lines = []
        file_data = open(self.path, 'r')
        for line in file_data:
            lines.append(line.strip())
            if sys.getsizeof(lines) > 128:
                self.partitions.extend(pt.Partition(lines, copy.copy(self.lazy)).action())
                lines = []
        file_data.close()
        if lines:
            self.partitions.extend(pt.Partition(lines, copy.copy(self.lazy)).action())
        return self.partitions

    def map(self, func):
        self.lazy.append((self.MAP, func))
        return self

    def filter(self, func):
        self.lazy.append((self.FILTER, func))
        return self

    def reduce(self, init_value, func):
        self.partitions = self.load()
        value = init_value
        for partition in self.partitions:
            value = partition.reduce(value, func)
        return value

    def reduceByKey(self, init_value, func):
        self.load()
        values = {}
        for partition in self.partitions:
            partition_files = partition.shuffle()
            for (key, files) in partition_files.items():
                for datum in files:
                    reduce_value = func(values.get(key, init_value), datum[1])
                    values[key] = reduce_value
        self.clear()
        self.partitions = [pt.Partition(sorted(values.items(), reverse=True))]
        return self

    def forEach(self, func):
        for partition in self.partitions:
            for value in partition.iter():
                func(value)
        self.clear()


def map_func(feature):
    return feature.split(',')[0], feature.split(',')[4]


def filter_func(value):
    return value[1] is '1'


def count(value_a, value_b):
    return int(value_a) + int(value_b)


def func(value):
    print(value)


rdd = RDD("../../data1")
rdd.map(map_func).filter(filter_func).reduceByKey(0, count).forEach(func)