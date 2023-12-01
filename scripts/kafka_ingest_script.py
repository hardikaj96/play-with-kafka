from confluent_kafka import Producer
import json
import time
from faker import Faker
import random
from datetime import datetime

# Kafka broker configuration
kafka_broker = 'kafka4:9092'
kafka_topic = 'example_topic'

# Create an instance of Faker
fake = Faker()

# Example data source (you can replace this with your actual data source logic)
def generate_data(num_rows=1, num_columns=10):
    data = []
    for _ in range(num_rows):
        current_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')

        # Generate random numeric values
        numeric_values = {
            'numeric_1': random.uniform(100, 200),
            'numeric_2': random.uniform(150, 250),
            'numeric_3': random.uniform(50, 100),
            'numeric_4': random.uniform(200, 300),
            'numeric_5': random.uniform(10, 50)
        }

        # Combine datetime and numeric values into a single dictionary
        row_data = {'datetime': current_datetime, **numeric_values}

        data.append(row_data)
    return data

# Function to initialize Kafka producer
def create_kafka_producer():
    producer_conf = {
        'bootstrap.servers': kafka_broker
    }
    producer = Producer(producer_conf)
    return producer

# Function to produce messages to Kafka topic
def produce_to_kafka(producer, data):
    for record in data:
        key = str(fake.uuid4())
        value = json.dumps(record)
        
        # Produce message to Kafka
        producer.produce(
            topic=kafka_topic,
            key=key,
            value=value
        )
        producer.flush()

        print(f"Produced message to {kafka_topic}: {record}")

# Main execution
if __name__ == "__main__":
    # Initialize Kafka producer
    kafka_producer = create_kafka_producer()

    try:
        while True:
            # Generate sample data
            data_to_ingest = generate_data(num_rows=1, num_columns=10)

            # Ingest data into Kafka topic
            produce_to_kafka(kafka_producer, data_to_ingest)

            # Sleep for one second before ingesting the next batch
            time.sleep(5)

    except KeyboardInterrupt:
        # Handle Ctrl+C to gracefully stop the producer
        pass

    finally:
        # Close the Kafka producer
        kafka_producer.flush()
        kafka_producer.close()
