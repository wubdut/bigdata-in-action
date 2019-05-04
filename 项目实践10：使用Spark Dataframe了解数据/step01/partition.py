# coding:utf-8
import uuid
import sys


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
