import json
import time

from kafka import KafkaProducer
from kafka.client import log
from kafka.errors import KafkaError
from pip._vendor import msgpack


# produce json messages
producer = KafkaProducer(value_serializer=lambda m: json.dumps(m).encode('ascii'))
future = producer.send('article', {'body': 'xxx', 'title': 'testje', 'timestamp': time.time()})


# Block for 'synchronous' sends
try:
    record_metadata = future.get(timeout=10)
    print(record_metadata)
except KafkaError:
    # Decide what to do if produce request failed...
    log.exception()
    pass
