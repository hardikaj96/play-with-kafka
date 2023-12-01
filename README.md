

# Play with Kafka

Welcome to the "play-with-kafka" project! This repository is designed for experimenting and learning with Kafka, a distributed streaming platform.

## Project Structure

The project is organized into the following components:

- **cluster-linking**: Configuration files for setting up Kafka clusters.
- **flask-app**: A Flask application for interacting with Kafka and showcasing functionalities.
- **schema-registry**: Scripts related to schema registry and Avro schema definition.
- **scripts**: Additional scripts for Kafka-related tasks.

## Getting Started

Follow these steps to get started with the "play-with-kafka" project:

1. Set up Kafka clusters using configurations in the `cluster-linking` directory.
2. Explore the Flask application in the `flask-app` directory to interact with Kafka.
3. Check out the scripts in the `scripts` directory for additional Kafka-related tasks.

## Usage

### Flask Application

1. Navigate to the `flask-app` directory.
2. Build the Docker image: `docker build -t play-with-kafka-app .`
3. Run the Flask application: `docker run -p 5000:5000 play-with-kafka-app`
4. Access the application at `http://localhost:5000` in your web browser.

### Kafka Scripts

Explore the scripts in the `scripts` directory for various Kafka-related tasks.

```bash
docker-compose exec -it kafka-scripts bash -c "python kafka_ingest_script.py"
docker-compose exec -it kafka-scripts bash -c "python kafka_consume_script.py"
```
