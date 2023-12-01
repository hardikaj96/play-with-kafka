from confluent_kafka import Consumer, KafkaError
from pymongo import MongoClient
import json

# Kafka broker configuration
kafka_broker = 'kafka:9092'
kafka_topic = 'example_topic'

# MongoDB configuration
mongo_uri = 'mongodb://root:example@mongo:27017'  # Replace with your MongoDB connection details
mongo_db_name = 'db'
mongo_collection_name = 'your_collection_name'

# Function to initialize Kafka consumer
def create_kafka_consumer():
    consumer_conf = {
        'bootstrap.servers': kafka_broker,
        'group.id': 'example_group',
        'auto.offset.reset': 'latest'  # Change to 'latest' if you want to consume only new messages
    }
    consumer = Consumer(consumer_conf)
    consumer.commit()
    return consumer

# Function to initialize MongoDB client
def create_mongo_client():
    return MongoClient(mongo_uri)

# Function to subscribe to Kafka topic and consume messages
def consume_from_kafka(consumer, mongo_client):
    # Subscribe to the Kafka topic
    consumer.subscribe([kafka_topic])

    # Connect to the MongoDB database and collection
    mongo_db = mongo_client[mongo_db_name]
    mongo_collection = mongo_db[mongo_collection_name]
    try:
        while True:
            # Poll for messages
            msg = consumer.poll(timeout=1000)  # Adjust timeout as needed
            consumer.commit()

            if msg is None:
                print('msg is none')
                continue
            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    # End of partition event
                    print("Reached end of partition, resetting consumer position.")
                    continue
                else:
                    # Handle other errors
                    print(f"Error: {msg.error()}")
                    break

            # Process the consumed message
            key = msg.key()
            value = msg.value()

            print(f"Consumed message from {kafka_topic}: Key={key}, Value={value}")

            # Insert the data into MongoDB
            document = json.loads(value.decode('utf-8'))
            mongo_collection.insert_one(document)

    except KeyboardInterrupt:
        # Handle Ctrl+C to gracefully stop the consumer
        pass

    finally:
        # Close the Kafka consumer and MongoDB client
        consumer.close()
        mongo_client.close()


# Main execution
if __name__ == "__main__":
    # Initialize Kafka consumer and MongoDB client
    kafka_consumer = create_kafka_consumer()
    mongo_client = create_mongo_client()
    try:
        # Consume messages from Kafka topic and insert into MongoDB
        consume_from_kafka(kafka_consumer, mongo_client)
    except KeyboardInterrupt:
        # Handle Ctrl+C to gracefully stop the consumer
        pass
