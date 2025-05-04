from confluent_kafka import Consumer, KafkaError, KafkaException
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.avro import AvroDeserializer
from confluent_kafka.serialization import SerializationContext, MessageField

import sys
import signal

KAFKA_BROKER = 'localhost:9092'
TOPIC_NAME = 'user-activity'
GROUP_ID = 'user-activity-group01'
SCHEMA_REGISTRY_URL = 'http://localhost:8081'
SCHEMA_ID=4

running = True

def shutdown_handler(signum, frame):
    global running
    running = False
    print("\n👋 Shutdown signal received. Closing Kafka consumer...")

def main():
    signal.signal(signal.SIGINT, shutdown_handler)
    signal.signal(signal.SIGTERM, shutdown_handler)

    # Schema Registry setup
    schema_registry_conf = {'url': SCHEMA_REGISTRY_URL}
    schema_registry_client = SchemaRegistryClient(schema_registry_conf)

    # ✅ Fetch schema string using schema ID
    try:
        schema_response = schema_registry_client.get_schema(schema_id=SCHEMA_ID)
        schema_str = schema_response.schema_str
        print(f"{schema_str}")
        
    except Exception as e:
        print(f"❌ Failed to fetch schema with ID {SCHEMA_ID}: {e}")
        sys.exit(1)

    # ✅ Initialize Avro deserializer with specific schema
    avro_deserializer = AvroDeserializer(
        schema_registry_client=schema_registry_client,
        schema_str=schema_str
    )

    # Always get the latest schema from the schema registry.
    # avro_deserializer = AvroDeserializer(
    #     schema_registry_client=schema_registry_client,
    #     schema_str=None  # None allows fetching schema by topic automatically
    # )

    # Kafka consumer config
    consumer_conf = {
        'bootstrap.servers': KAFKA_BROKER,
        'group.id': GROUP_ID,
        'auto.offset.reset': 'earliest',
        'enable.auto.commit': True,
        'client.id': 'python-consumer'
    }

    consumer = Consumer(consumer_conf)

    try:
        consumer.subscribe([TOPIC_NAME])
        print(f"✅ Subscribed to topic: {TOPIC_NAME}")
        print(f"🔁 Waiting for messages from Kafka at {KAFKA_BROKER}...\n")

        while running:
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                if msg.error().code() != KafkaError._PARTITION_EOF:
                    print(f"⚠️ Error: {msg.error()}")
                continue

            try:
                # Deserialize value using AvroDeserializer
                user_acitivity = avro_deserializer(
                    msg.value(),
                    SerializationContext(TOPIC_NAME, MessageField.VALUE)
                )
                print(f" User Activity {user_acitivity}")
            except Exception as e:
                print(f"❌ Deserialization failed: {e}")

    except KafkaException as e:
        print(f"KafkaException: {e}")
    except Exception as ex:
        print(f"Unexpected error: {ex}")
    finally:
        consumer.close()
        print("✅ Consumer closed cleanly.")

if __name__ == '__main__':
    main()
