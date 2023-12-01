from confluent_kafka import Producer
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.avro import AvroSerializer
from confluent_kafka.serialization import (
   SerializationContext,
   MessageField,
)
import time

schema_registry_conf = {'url': 'http://localhost:8081'}
schema_registry_client = SchemaRegistryClient(schema_registry_conf)

with open("telemetry.avsc") as f:
   value_schema = f.read()

avro_serializer = AvroSerializer(schema_registry_client, value_schema)

producer_conf = {'bootstrap.servers': 'localhost:19092'}
producer = Producer(producer_conf)

topic = "my_topic2"

# Sample data to produce
messages = [
    {"id": 4, "value": "Message 1"},
    {"id": 5, "value": "Message 2"},
    {"id": 6, "value": "Message 3"}
]

# Produce messages
for message in messages:
    print(message)
    producer.produce(
        topic=topic,
        value=avro_serializer(message, SerializationContext(topic, MessageField.VALUE)),
    )
    producer.flush()
    time.sleep(1)
    