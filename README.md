# 🎬 Kafka Movie Producer & Consumer

This project contains a Python-based Kafka **Producer** and **Consumer** that communicate via a Kafka topic called `hit-movies-v2`. Messages are sent and received as key-value pairs, e.g., `2001: movie1`.

---

## 🛠️ Requirements

- Python 3.7+
- Kafka running on `172.17.0.1:9092`
- [Confluent Kafka Python client](https://docs.confluent.io/platform/current/clients/confluent-kafka-python/html/index.html)

Install dependencies:

```bash
pip install confluent-kafka
```

## ⚙️ Kafka Configuration

Ensure your Kafka broker is correctly configured with:

listeners=PLAINTEXT://0.0.0.0:9092
advertised.listeners=PLAINTEXT://172.17.0.1:9092

## 🚀 Usage

# 🧾 Producer

Sends key-value messages (e.g. 2001: movie1) to the Kafka topic.

```bash
python producer.py
```

Example output:

✅ Topic "hit-movies-v2" exists.
✅ Connected to Kafka at 172.17.0.1:9092
📤 Sent message: Key=2001, Value=movie1

# 📦 Consumer

Listens to messages on the hit-movies-v2 topic and prints them.

```bash
python consumer.py
```

# Example output:

✅ Subscribed to topic: hit-movies-v2
📦 Received message | Key: 2001 | Value: movie1

## 🧪 Testing

To verify everything is working:

```bash
    Run the consumer first: python consumer.py

    Then run the producer: python producer.py

    Watch the consumer receive messages in real-time.
```
