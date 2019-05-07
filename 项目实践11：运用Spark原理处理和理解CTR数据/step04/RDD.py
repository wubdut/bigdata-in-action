# coding:utf-8
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
                self.partitions.extend(Partition(lines, copy.copy(self.lazy)).action())
                lines = []
        file_data.close()
        if lines:
            self.partitions.extend(Partition(lines, copy.copy(self.lazy)).action())
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
        self.partitions = [Partition(sorted(values.items(), reverse=True))]
        return self

    def forEach(self, func):
        for partition in self.partitions:
            for value in partition.iter():
                func(value)
        self.clear()


def map_func(feature):
    return feature.split(',')[0], feature.split(',')[-1]


def filter_func(value):
    return value[1] is '1'


def count(value_a, value_b):
    return int(value_a) + int(value_b)


def func(value):
    print(value)


if __name__ == '__main__':
    rdd = RDD("../data")
    rdd.map(map_func).filter(filter_func).reduceByKey(0, count).forEach(func)