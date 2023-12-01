from confluent_kafka import avro
from confluent_kafka.avro import AvroProducer

# Schema Registry URL
schema_registry_url = "http://localhost:8081"

# Kafka broker URL
bootstrap_servers = "localhost:19092"

# Avro schema definition
avro_schema_str = """
{
  "type": "record",
  "name": "example",
  "fields": [
    {"name": "id", "type": "int"},
    {"name": "value", "type": "string"}
  ]
}
"""

# Create Avro schema object
avro_schema = avro.loads(avro_schema_str)

# Create AvroProducer configuration
avro_producer_config = {
    'bootstrap.servers': bootstrap_servers,
    'schema.registry.url': schema_registry_url
}

# Create AvroProducer instance
avro_producer = AvroProducer(avro_producer_config, default_value_schema=avro_schema)

# Topic to produce messages to
topic = "your_topic"

# Sample data to produce
messages = [
    {"id": 1, "value": "Message 1"},
    {"id": 2, "value": "Message 2"},
    # {"id": "4", "value": "Message 4"},
    {"id": 3, "value": "Message 3"}
]

# Produce messages
for message in messages:
    avro_producer.produce(topic=topic, value=message)

    # Wait for any outstanding messages to be delivered and delivery reports received
    avro_producer.flush()

print("Messages produced successfully.")
