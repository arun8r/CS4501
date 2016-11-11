from kafka import KafkaConsumer
from kafka import KafkaProducer
from elasticsearch import Elasticsearch
import json

print ("hey whats up")

elasticsearch = Elasticsearch([{'host': 'elasticsearch', 'port': 9200}])
consumer = KafkaConsumer('new-listings-topic', group_id='listing-indexer', bootstrap_servers=['kafka:9092'])
for message in consumer:
    new_sale = (json.loads((message.value).decode('utf-8')))
    
    print(message)
    ret = elasticsearch.index(index='listing-indexer',doc_type = 'listing',id = new_sale['id'])
    elasticsearch.indices.refresh(index="listing-indexer")
    print("hello from the indexer")