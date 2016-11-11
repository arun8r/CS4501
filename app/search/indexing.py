from kafka import KafkaConsumer
from kafka import KafkaProducer
from elasticsearch import Elasticsearch
import json
import time


time.sleep(30)
es = Elasticsearch(['es'])
consumer = KafkaConsumer('new-listings-topic', group_id='listing-indexer', bootstrap_servers=['kafka:9092'])
for message in consumer:
    new_sale = (json.loads((message.value).decode('utf-8')))
    ret = es.index(index='listing-indexer',doc_type = 'listing',id = new_sale['id'], body = new_sale)
    es.indices.refresh(index="listing-indexer")
