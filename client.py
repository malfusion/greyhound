import json
from kafka import KafkaProducer
import datetime

producer = KafkaProducer(bootstrap_servers='kafka:9092')


for i in range(10000, 30000):
    producer.send('spans', json.dumps({
        'span_id': i,
        'parent_span_id': 1,
        'process_id': 75,
        'cont_id': 100,
        'start_time': str(datetime.datetime.now()),
        'tags': []
    }).encode('utf-8'))


    producer.send('spans', json.dumps({
        'span_id': i,
        'parent_span_id': 1,
        'process_id': 75,
        'cont_id': 100,
        'end_time': str(datetime.datetime.now()),
        'tags': []
    }).encode('utf-8'))

producer.flush()