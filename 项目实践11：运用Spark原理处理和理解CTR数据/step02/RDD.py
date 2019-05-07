# coding:utf-8

import uuid
import os
import sys
import copy


class Partition:

    def __init__(self, partition_data=[], lazy=[], tmp_dir="tmp"):
        self.partition_data = partition_data
        self.lazy = lazy
        self.tmp_dir = tmp_dir
        self.partition_path = []
        self.iterators = []
        self.write()

    def iter(self):
        iter_data = []
        for file in self.partition_path:
            partition_data = open(file, 'r')
            for datum in partition_data:
                iter_data.append(datum.strip())
        return iter_data

    def clear(self):
        self.iterators = []
        self.partition_data = []
        for path in self.partition_path:
            os.remove(path)

    def write(self):
        name_partition = str(uuid.uuid4())
        file_partition = open(os.path.join(self.tmp_dir, name_partition), "a")
        file_partition.write("\n".join(self.partition_data))
        file_partition.close()
        self.partition_path.append(os.path.join(self.tmp_dir, name_partition))
        self.partition_data = []

    def map(self, func):
        reduce_partitions = []
        data = []
        for datum in self.iter():
            if datum:
                data.append(func(datum))
            if sys.getsizeof(data) > 1024 * 1024 * 5:
                reduce_partitions.extend(Partition(data, copy.copy(self.lazy)).action())
                data = []
        if data:
            reduce_partitions.extend(Partition(data, copy.copy(self.lazy)).action())
        return reduce_partitions

    def filter(self, func):
        reduce_partitions = []
        data = []
        for datum in self.iter():
            if func(datum):
                data.append(datum)
            if sys.getsizeof(data) > 1024 * 1024 * 5:
                reduce_partitions.extend(Partition(data, copy.copy(self.lazy)).action())
        if data:
            reduce_partitions.extend(Partition(data, copy.copy(self.lazy)).action())
        return reduce_partitions

    def reduce(self, value, func):
        for datum in self.iter():
            value = func(value, datum)
        self.clear()
        self.partition_data = [value]
        return str(value)

    def action(self):
        if self.lazy:
            op = self.lazy[0]
            self.lazy.remove(op)
            if op[0] is "map":
                return self.map(op[1])
            if op[0] is "filter":
                return self.filter(op[1])
            raise Exception("Unsupported action %s" % op[0])
        self.write()
        return [self]


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
            reduce_partitions.extend(Partition(lines, copy.copy(self.lazy)).action())
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


if __name__ == '__main__':
    rdd = RDD("../data")
    print("垃圾广告数量为：%s\n" % rdd.map(map_func).filter(filter_func).reduce(0, count))
