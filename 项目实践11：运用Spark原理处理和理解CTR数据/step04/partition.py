# coding:utf-8
import bisect
import uuid
import os
import sys
import copy
import pickle


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
            partition_data = pickle.load(open(file, 'rb'))
            for datum in partition_data:
                iter_data.append(datum)
        return iter_data

    def clear(self):
        self.iterators = []
        self.partition_data = []
        for path in self.partition_path:
            os.remove(path)

    def write(self):
        name_partition = str(uuid.uuid4())
        file_partition = open(os.path.join(self.tmp_dir, name_partition), "wb")
        pickle.dump(self.partition_data, file_partition)
        file_partition.close()
        self.partition_path.append(os.path.join(self.tmp_dir, name_partition))
        self.partition_data = []

    def map(self, func):
        reduce_partitions = []
        data = []
        for datum in self.iter():
            if datum:
                data.append(func(datum))
            if sys.getsizeof(data) > 1024:
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

    def reduce(self, init_value, func):
        value = init_value
        for datum in self.iter():
            value = func(value, datum)
        self.clear()
        self.partition_data = [value]
        return str(value)

    def shuffle(self):
        values = {}
        for datum in self.iter():
            file = values.get(datum[0], [])
            file.append(datum)
            values[datum[0]] = file
        return values

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
