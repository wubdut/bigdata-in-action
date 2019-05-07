# coding:utf-8

import uuid
import os
import sys
import random


class Partition:

    def __init__(self, lines, tmp_path="tmp/"):
        self.tmp_path = tmp_path
        self.partition = self.write(lines)

    def write(self, lines):
        name_partition = str(uuid.uuid4())
        file_partition = open(self.tmp_path + name_partition, "a")
        file_partition.write("\n".join(lines))
        file_partition.close()
        return self.tmp_path + name_partition

    def map(self, func):
        partitions = []
        partition_data = open(self.partition, 'r')
        lines = []
        for line in partition_data:
            if line.strip():
                lines.append(func(line.strip()))
            if sys.getsizeof(lines) > 1024 * 1024 * 5:
                partitions.append(Partition(lines))
                lines = []

        if len(lines) > 0:
            partitions.append(Partition(lines))

        return partitions

    def filter(self, func):
        partitions = []
        partition_data = open(self.partition, 'r')
        lines = []
        for line in partition_data:
            if func(line.strip()):
                lines.append(line.strip())
            if sys.getsizeof(lines) > 1024 * 1024 * 5:
                partitions.append(Partition(lines))
                lines = []
        if lines:
            partitions.append(Partition(lines))

        return partitions

    def foreach(self, func):
        partition_data = open(self.partition, 'r')
        for line in partition_data:
            func(line)


class RDD:

    def __init__(self, path, tmp_path="tmp/"):
        print('create RDD')

        self.partitions = []

        ls = os.listdir(tmp_path)
        for name_file in ls:
            os.remove(os.path.join(tmp_path, name_file))

        self.tmp_path = tmp_path

        lines = []
        file_data = open(path, 'r')
        for line in file_data:
            lines.append(line)
            if sys.getsizeof(lines) > 1024 * 1024 * 5:
                self.partitions.append(pt.Partition(lines, tmp_path))
                lines = []

        if lines:
            self.partitions.append(Partition(lines, tmp_path))
        file_data.close()

    def copy(self):
        self.partitions = []

    def map(self, func):
        tmp_partitions = self.partitions.copy()
        self.partitions = []
        for partition in tmp_partitions:
            self.partitions.extend(partition.map(func))
            os.remove(partition.partition)
        return self

    def filter(self, func):
        tmp_partitions = self.partitions.copy()
        self.partitions = []
        for partition in tmp_partitions:
            self.partitions.extend(partition.filter(func))
            os.remove(partition.partition)
        return self

    def foreach(self, func):
        for partition in self.partitions:
            partition.foreach(func)
            os.remove(partition.partition)


def map_func(feature):
    vec = feature.split(',')
    vec.append(str(random.uniform(0, 1)))
    return ",".join(vec)


def train_filter_func(value):
    return float(value.split(',')[-1]) < 0.8


def test_filter_func(value):
    return float(value.split(',')[-1]) >= 0.8


def count(value_a, value_b):
    return int(value_a) + int(value_b)


def foreach_func(value):
    print(value.strip())


if __name__ == '__main__':
    rdd = RDD("../data")
    rdd = rdd.map(map_func)
    rdd.filter(test_filter_func).foreach(foreach_func)
