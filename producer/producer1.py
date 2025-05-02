from confluent_kafka import Producer, KafkaException, KafkaError, admin
import sys
import time

KAFKA_BROKER = 'localhost:9092'
TOPIC_NAME = 'hit-movies-v2'

def delivery_report(err, msg):
    """ Called once for each message to confirm delivery or error """
    if err is not None:
        print(f'❌ Delivery failed: {err}')
    else:
        print(f'✅ Message delivered to {msg.topic()} [{msg.partition()}] @ offset {msg.offset()}')

def check_topic_exists(admin_client, topic_name):
    """ Check if a topic exists in Kafka """
    try:
        metadata = admin_client.list_topics(timeout=10)
        for broker in metadata.brokers.values():
          print(f"Broker ID: {broker.id}, Host: {broker.host}, Port: {broker.port}")

        return topic_name in metadata.topics
    except Exception as e:
        print(f'⚠️ Failed to fetch topic metadata: {e}')
        return False

def main():
    # Configure Kafka producer
    conf = {
        'bootstrap.servers': KAFKA_BROKER,
        'client.id': 'python-producer-1'
    }

    try:
        # Admin client for topic check
        admin_client = admin.AdminClient({'bootstrap.servers': KAFKA_BROKER})
        if not check_topic_exists(admin_client, TOPIC_NAME):
            print(f'❌ Topic "{TOPIC_NAME}" does not exist.')
            sys.exit(1)
        else:
            print(f'✅ Topic "{TOPIC_NAME}" exists.')

        # Create producer
        producer = Producer(conf)
        print(f'✅ Connected to Kafka at {KAFKA_BROKER}')

        # Example message: key = 2001, value = movie1
        messages = {
            '2001': 'movie4',
            '2002': 'movie5',
            '2003': 'movie6'
        }

        for key, value in messages.items():
            producer.produce(
                topic=TOPIC_NAME,
                key=key,
                value=value,
                callback=delivery_report
            )
            producer.poll(0)  # Trigger callback

        producer.flush()

    except KafkaException as ke:
        print(f'KafkaException: {ke}')
    except Exception as e:
        print(f'Unhandled exception: {e}')
    finally:
        print('👋 Producer script finished.')

if __name__ == '__main__':
    main()

