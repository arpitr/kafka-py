# Kafka Connect Custom SMT - RegexFilter

This project provides a custom Kafka Connect Single Message Transform (SMT) plugin called `RegexFilter`. The `RegexFilter` SMT allows you to filter Kafka records based on a regular expression applied to the record's value.

## Features

- Filters Kafka records based on a user-defined regular expression.
- Keeps only the records that match the regex.
- Can be used with any Kafka Connect source or sink connector.

## Requirements

- Java 8 or higher
- Maven
- Kafka Connect 3.5.0 or compatible version

## Installation

### 1. Build the Plugin

Clone the repository and build the JAR file:

```bash
cd kafka-connect-custom-smt
mvn clean package
```

The JAR file will be generated in the `target/` directory:

```bash
target/kafka-connect-custom-smt-1.0-SNAPSHOT.jar**
```

### 2. Deploy the Pl

- Make sure to following configuration in docker compose. Refer to https://github.com/arpitr/kafka-py/blob/master/connect/docker-compose.yml#L54
- This will automatically sync the plugin to docker container on next container restart.

```bash
volumes:

- ./connectors:/usr/share/confluent-hub-components
```

### 3. Restart Docker container

```
docker-compose restart
```

### 4. Enable the plugin

```bash
# Install Spooldir Source Connector.
curl -X POST http://localhost:8083/connectors -H "Content-Type: application/json" -d @spooldir_line_source_config.json
# Install JDBC Sink Connector.
curl -X POST http://localhost:8083/connectors -H "Content-Type: application/json" -d @kafka_postgres_sink_with_smt.json
```

### 5. Create table in postgres database.

```bash
psql -h localhost -U postgres -d postgres
CREATE TABLE webserver_logs (
    raw_log TEXT
);
```

## Testing

1. Generate Error logs, https://www.kaggle.com/datasets/vishnu0399/server-logs and place the log file(*.log) under cp-all-in-one/cp-all-in-one-kraft/spooldir/input.
2. Check Kafka Control Panel to see logs inside topic webserver.logs
3. Check Postgres database to see records are added inside webserver_logs in raw_log field filtered with pattern mention in kafka_postgres_sink_with_smt.json
