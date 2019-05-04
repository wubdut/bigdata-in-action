import os
from kafka import KafkaConsumer
import random


output_dir = os.path.join('/home/demo/data/', 'split')
output_dict = {}
for i in range(0, 10):
    output_dict[i] = open(os.path.join(output_dir, 'part-%05d' % i), 'w')

consumer = KafkaConsumer('test4', bootstrap_servers=['localhost:9092'])
for message in consumer:
    rand_int = random.randint(0, 9)
    output_dict[rand_int].write(message.value.decode('utf8') + '\n')

