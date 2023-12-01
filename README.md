

# Play with Kafka

Welcome to the "play-with-kafka" project! This repository is designed for experimenting and learning with Kafka, a distributed streaming platform.

## Project Structure

The project is organized into the following components:

- **cluster-linking**: Configuration files for setting up Kafka clusters.
- **schema-registry**: Scripts related to schema registry and Avro schema definition.
- **flask-app**: Whole system

## Getting Started

Follow these steps to get started with the "play-with-kafka" project:

## Usage

Please make sure, docker and docker-compose are installed

### Application

Run the main application
```
docker-compose up -d
```
This will start 1 zookeeper instance running on Port 2181 and 3 kafka broker containers running on Port 9092, 9093 and 9094.
It will also start Mongo container on port 27017 with default db and collection created.
It will start the Flask App which will show [live timeseries chart!](image.png)

#### Kafka Scripts

Start the scripts in the `scripts` directory for Producer-Consumer scripts.

```bash
docker-compose exec -it kafka-scripts bash -c "python kafka_ingest_script.py"
docker-compose exec -it kafka-scripts bash -c "python kafka_consume_script.py"
```

The live timeseries will start showing up the data being produced by the Producer.
