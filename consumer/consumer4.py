from confluent_kafka import Consumer, KafkaError, KafkaException
import sys
import signal

KAFKA_BROKER = 'localhost:9092'
TOPIC_NAME = 'hit-movies-v2'
GROUP_ID = 'movie-consumer-group-2'

# Graceful exit flag
running = True

def shutdown_handler(signum, frame):
    global running
    running = False
    print("\n👋 Shutdown signal received. Closing Kafka consumer...")

def main():
    # Handle CTRL+C / SIGTERM
    signal.signal(signal.SIGINT, shutdown_handler)
    signal.signal(signal.SIGTERM, shutdown_handler)

    # Kafka Consumer config
    conf = {
        'bootstrap.servers': KAFKA_BROKER,
        'group.id': GROUP_ID,
        'auto.offset.reset': 'earliest',  # Or 'latest'
        'enable.auto.commit': True,
        'client.id': 'python-consumer-4'
    }

    consumer = Consumer(conf)

    try:
        consumer.subscribe([TOPIC_NAME])
        print(f"✅ Subscribed to topic: {TOPIC_NAME}")
        print(f"🔁 Waiting for messages from Kafka at {KAFKA_BROKER}...\n")

        while running:
            msg = consumer.poll(1.0)  # Wait for 1 second

            if msg is None:
                continue
            if msg.error():
                if msg.error().code() != KafkaError._PARTITION_EOF:
                    print(f"⚠️ Error: {msg.error()}")
                continue

            print(f"📦 Received message | Key: {msg.key().decode('utf-8') if msg.key() else 'None'} | "
                  f"Value: {msg.value().decode('utf-8')}")

    except KafkaException as e:
        print(f"KafkaException: {e}")
    except Exception as ex:
        print(f"Unexpected error: {ex}")
    finally:
        consumer.close()
        print("✅ Consumer closed cleanly.")

if __name__ == '__main__':
    main()

