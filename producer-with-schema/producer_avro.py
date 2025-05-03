#!/usr/bin/env python3
from confluent_kafka import Producer, KafkaException, KafkaError, admin
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.avro import AvroSerializer, AvroDeserializer
from confluent_kafka.serialization import SerializationContext, MessageField
import sys
import time
import json
import requests
from datetime import datetime

# Configuration
KAFKA_BROKER = 'localhost:9092'
SCHEMA_REGISTRY_URL = 'http://localhost:8081'
TOPIC_NAME = 'user-activity'
SCHEMA_ID = 2  # Using pre-registered schema with ID 1

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

def get_user_activity_data():
    """ Sample user acitivty data to be produced - format must match the registered schema """
    current_timestamp = int(datetime.now().timestamp() * 1000)

    url = 'http://localhost:9999/user-activities'

    try:
        # Send GET request
        response = requests.get(url)
        
        # Raise an exception for bad status codes
        response.raise_for_status()

        # Parse and print the JSON response
        data = response.json()
        print(f"User Activities:{data}")

    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
    
    return data

def main():
    # Configure Kafka producer
    producer_conf = {
        'bootstrap.servers': KAFKA_BROKER,
        'client.id': 'python-avro-producer'
    }

    # Configure Schema Registry client
    schema_registry_conf = {'url': SCHEMA_REGISTRY_URL}

    try:
        # Admin client for topic check
        admin_client = admin.AdminClient({'bootstrap.servers': KAFKA_BROKER})
        if not check_topic_exists(admin_client, TOPIC_NAME):
            print(f'❌ Topic "{TOPIC_NAME}" does not exist.')
            sys.exit(1)
        else:
            print(f'✅ Topic "{TOPIC_NAME}" exists.')

        # Create Schema Registry client
        schema_registry_client = SchemaRegistryClient(schema_registry_conf)
        
        # Fetch the schema by ID from the registry
        try:
            schema = schema_registry_client.get_schema(SCHEMA_ID)
            print(f'✅ Successfully retrieved schema with ID: {SCHEMA_ID}')
            print(f'   Schema type: {schema.schema_type}')
            print(f'   Schema: {schema.schema_str[:60]}...')  # Print first 60 chars
            
            # Create Avro serializer using the fetched schema
            avro_serializer = AvroSerializer(
                schema_registry_client,
                schema.schema_str,
                lambda user_activity, ctx: user_activity
            )
            
        except Exception as e:
            print(f'❌ Failed to retrieve schema with ID {SCHEMA_ID}: {e}')
            sys.exit(1)
        
        # Create producer
        producer = Producer(producer_conf)
        print(f'✅ Connected to Kafka at {KAFKA_BROKER}')

        # Get user activity data to produce
        user_activities = get_user_activity_data()
        
        # Check if data matches schema
        print('🔄 Serializing User Activity data with pre-registered schema...')

        for user_activity in user_activities:
            # User ID will be the message key
            
            try:
                # Serialize the user activity record using Avro
                value = avro_serializer(
                    user_activity, 
                    SerializationContext(TOPIC_NAME, MessageField.VALUE)
                )
                
                # Produce message
                producer.produce(
                    topic=TOPIC_NAME,
                    value=value,
                    callback=delivery_report
                )
                producer.poll(0)  # Trigger callback
                
            except Exception as e:
                print(f'❌ Error producing message for user activity {key}: {e}')
                # Continue with next user activity instead of terminating the whole process
                continue

        producer.flush()
        print(f'✅ Attempted to produce {len(user_activities)} messages with Avro serialization')

    except KafkaException as ke:
        print(f'KafkaException: {ke}')
    except Exception as e:
        print(f'Unhandled exception: {e}')
    finally:
        print('👋 Producer script finished.')

if __name__ == '__main__':
    main()
