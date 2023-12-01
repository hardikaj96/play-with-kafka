from confluent_kafka import Consumer
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.avro import AvroDeserializer
from confluent_kafka.serialization import (
  SerializationContext,
  MessageField,
)

schema_registry_conf = {'url': 'http://localhost:8081'}
schema_registry_client = SchemaRegistryClient(schema_registry_conf)

with open("telemetry.avsc") as f:
  value_schema = f.read()

avro_deserializer = AvroDeserializer(schema_registry_client, value_schema)

consumer_conf = {
   'bootstrap.servers': 'localhost:19092',
   'group.id': 'mygroup1',
   'auto.offset.reset': 'earliest'
}
consumer = Consumer(consumer_conf)
topic = "my_topic2"


# Subscribe to the topic
consumer.subscribe([topic])

try:
    while True:
        # Poll for messages
        msg = consumer.poll(1.0)  # Adjust the timeout as needed

        message = consumer.poll(1.0)
        if message is None:
            continue
        if message.error():
            print("Consumer error: {}".format(message.error()))
            continue

        # Deserialize the value
        value = avro_deserializer(message.value(), SerializationContext(topic, MessageField.VALUE))

        # Process the message (replace with your logic)
        print(f"Received message: {value}")

except KeyboardInterrupt:
    pass
finally:
    # Close down consumer to commit final offsets.
    consumer.close()
