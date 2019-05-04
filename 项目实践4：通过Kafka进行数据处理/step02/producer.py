import sys
from kafka import KafkaProducer

data_path = '/home/demo/data/temp'

producer = KafkaProducer(bootstrap_servers='localhost:9092')

line_num = 0
for line in open(data_path):
    line_num += 1
    if line_num == 1:
        continue

    if line_num % 1000 == 0:
        sys.stdout.write("\r%d" % line_num)
        sys.stdout.flush()
        producer.flush()

    producer.send('test4', line.strip().encode('utf8'))
producer.flush()
