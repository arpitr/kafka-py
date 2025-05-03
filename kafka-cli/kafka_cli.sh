#!/bin/bash

# Kafka Topics
kafka-topics --create --bootstrap-server localhost:9092 --topic hit-movies --partitions 3 --replication-factor 1
kafka-topics --list --bootstrap-server localhost:9092
kafka-topics --describe --bootstrap-server localhost:9092 --topic hit-movies
kafka-topics --bootstrap-server localhost:9092 --alter --topic hit-movies --partitions 5

# Kafka Producer
kafka-console-producer --bootstrap-server localhost:9092 --topic hit-movies --partitions 3
kafka-console-producer --bootstrap-server localhost:9092 --topic hit-movies --property "parse.key=true" --property "key.separator=:"


# Kafka Consumer
kafka-console-consumer --bootstrap-server localhost:9092 --topic hit-movies --group consumer-group-1
