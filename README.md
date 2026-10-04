# Smart Order Event Processing System using Apache Kafka

A beginner-friendly distributed event-processing project built using Python, Apache Kafka, SQLite, Docker, and automated testing.

## Project Overview

This project demonstrates how an order event can be produced, sent through an Apache Kafka topic, consumed by a Python consumer, validated, and stored in a SQLite database.

## Architecture

```
Python Producer
      |
      | JSON Order Events
      v
Apache Kafka
  orders topic
      |
      v
Python Consumer
      |
      v
Order Validation
      |
      v
SQLite Database

```

## Technologies Used
- Python
- Apache Kafka
- Docker
- SQLite
- pytest
- GitHub Actions

## Project Flow
1. The Python producer creates sample order events.
2. Orders are published to the Kafka orders topic.
3. The Python consumer receives the events.
4. Each order is validated.
5. Valid orders are stored in SQLite.
6. Automated tests verify event validation and database operations.

## Sample Orders
- Order 1001 - Rahul - Laptop - 55000
- Order 1002 - Priya - Mouse - 1200
- Order 1003 - Aman - Phone - 25000

## Testing

The project contains automated tests for:

- Order validation
- Invalid order rejection
- JSON encoding and decoding
- Database creation
- Order storage

Run tests using:

python -m pytest -v

## Running the Project

Start Kafka using Docker Compose:

docker compose up -d

Create the Kafka topic:

docker exec smart-order-kafka /opt/kafka/bin/kafka-topics.sh --create --topic orders --bootstrap-server localhost:9092

Start the consumer:

python -m consumer.consumer

In another terminal, run the producer:

python producer/producer.py

The consumer processes the order events and stores them in SQLite.

## CI/CD

GitHub Actions is used to automatically run the project's test suite whenever code is pushed to the repository or a pull request is created.

## Author

BTech CSE Student