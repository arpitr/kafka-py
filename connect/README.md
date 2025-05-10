# Kafka-Py Connect

Kafka Connect allows to connect 
- Upstream data sources from where kafka connectors will pull the messages and store in Kafka topics.
- Downstream  sink applications where kafka connectors will push data after reading from kafka topics.


## Connectors Used

- [Kafka Connect Spooldir](https://www.confluent.io/hub/confluentinc/kafka-connect-spooldir): Allows to read file from file system and push to kafka topic
- [JDBC Connector (Source and Sink)](https://www.confluent.io/hub/confluentinc/kafka-connect-jdbc) : Allows to kafka topic and 


flowchart TD
    A[logfile.log in Filesystem] -->|Kafka Connect Spooldir| B[Kafka Topic: webserver.logs]
    B -->|JDBC Connector| C[Postgres Server (localhost:5432)]


## Prerequisites
- [Kafka](https://github.com/confluentinc/cp-all-in-one/) is running on local
```bash
cd cp-all-in-one/cp-all-in-one-kraft/
docker-compose up -d
```
- [Postgres](https://hub.docker.com/_/postgres)
```bash
  ~ docker run -d \
  --name local-postgres \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=postgres \
  -e POSTGRES_DB=postgres \
  -p 5432:5432 \
  -v pgdata:/var/lib/postgresql/data \
  postgres
```
- Kafka Connect is running on localhost:8083
- Postgres is running on localhost:5432


## Installation
1. Download the connectors from confluent hub on link mentioned earlier.
2. Update docker-compose file for kafka installation to match https://github.com/arpitr/kafka-py/blob/master/connect/docker-compose.yml
3. Notice the volumes mounted for connectors
```bash
    volumes:
      - ./connectors:/usr/share/confluent-hub-components
      - ./spooldir/input:/opt/kafka-connect/spooldir/input
      - ./spooldir/finished:/opt/kafka-connect/spooldir/finished
      - ./spooldir/error:/opt/kafka-connect/spooldir/error
```
4. Make sure the downloaded connectors are placed under cp-all-in-one/cp-all-in-one-kraft/connectors.
5. Check if the plugins are available
```bash
curl -S localhost:8083/connector-plugins | jq .
```
6. Install the plugins
```bash
# Install Spooldir Source Connector.
curl -X POST http://localhost:8083/connectors -H "Content-Type: application/json" -d @spooldir_line_source_config.json
# Install JDBC Sink Connector.
curl -X POST http://localhost:8083/connectors -H "Content-Type: application/json" -d @kafka_postgres_sink.json
```
7. Create table in postgres database.
```bash
psql -h localhost -U postgres -d postgres
CREATE TABLE webserver_logs (
    raw_log TEXT
);
```

## Testing
1. Generate Error logs, https://www.kaggle.com/datasets/vishnu0399/server-logs and place the log file(*.log) under cp-all-in-one/cp-all-in-one-kraft/spooldir/input.
2. Check Kafka Control Panel to see logs inside topic webserver.logs
3. Check Postgres database to see records are added inside webserver_logs in raw_log field.

