#!/usr/bin/env python3
"""
Script to register a schema with Kafka Schema Registry
"""

import json
import argparse
import requests
import sys
from typing import Dict, Any, Optional


class SchemaRegistry:
    def __init__(self, url: str):
        """Initialize Schema Registry client.

        Args:
            url: Schema Registry URL (e.g., http://localhost:8081)
        """
        self.url = url.rstrip('/')

    def register_schema(self,
                        subject: str,
                        schema: Dict[str, Any],
                        schema_type: str = "AVRO",
                        compatibility: Optional[str] = None) -> int:
        """Register a schema with the Schema Registry.

        Args:
            subject: Name of the subject (typically topic-key or topic-value)
            schema: Schema definition as a dictionary
            schema_type: Schema type ("AVRO", "JSON", "PROTOBUF")
            compatibility: Optional compatibility level

        Returns:
            Schema ID assigned by the registry
        """
        # Convert schema dictionary to JSON string if it's not already
        if isinstance(schema, dict):
            schema = json.dumps(schema)

        # Prepare request payload
        payload = {
            "schema": schema,
            "schemaType": schema_type
        }

        # Make the request to register the schema
        response = requests.post(
            f"{self.url}/subjects/{subject}/versions",
            headers={"Content-Type": "application/vnd.schemaregistry.v1+json"},
            json=payload
        )

        # Check if request was successful
        response.raise_for_status()

        # Parse the response
        result = response.json()
        schema_id = result.get("id")

        # Set compatibility if provided
        if compatibility:
            self.set_compatibility(subject, compatibility)

        return schema_id

    def delete_subject(self, subject):
        url = f"{self.url}/subjects/{subject}"
        response = requests.delete(url)

        if response.status_code == 200:
            print(f"Successfully deleted subject '{subject}': Versions {response.json()}")
        elif response.status_code == 404:
            print(f"Subject '{subject}' not found.")
        else:
            print(f"Failed to delete subject '{subject}': {response.status_code} {response.text}")

    def set_compatibility(self, subject: str, compatibility: str) -> None:
        """Set compatibility level for a subject.

        Args:
            subject: Name of the subject
            compatibility: Compatibility level (BACKWARD, FORWARD, FULL, NONE)
        """
        response = requests.put(
            f"{self.url}/config/{subject}",
            headers={"Content-Type": "application/vnd.schemaregistry.v1+json"},
            json={"compatibility": compatibility}
        )
        response.raise_for_status()


def main():
    parser = argparse.ArgumentParser(description="Register schema with Kafka Schema Registry")
    parser.add_argument("--registry-url", required=True, help="Schema Registry URL")
    parser.add_argument("--subject", required=True, help="Subject name (typically topic-key or topic-value)")
    parser.add_argument("--schema-file", required=True, help="Path to schema file (JSON format)")
    parser.add_argument("--schema-type", default="AVRO", choices=["AVRO", "JSON", "PROTOBUF"],
                        help="Schema type (default: AVRO)")
    parser.add_argument("--compatibility", choices=["BACKWARD", "FORWARD", "FULL", "NONE"],
                        help="Compatibility level (optional)")
    parser.add_argument("--delete", default=False, action='store_true',help="Delete Schema")

    args = parser.parse_args()
    print(f"{args.delete}")


    # Register schema
    registry = SchemaRegistry(args.registry_url)
    try:
        if args.delete is not True:
            # Load schema from file
            with open(args.schema_file, 'r') as f:
                schema = json.load(f)
            schema_id = registry.register_schema(
                args.subject,
                schema,
                args.schema_type,
                args.compatibility
            )
            print(f"Schema registered successfully with ID: {schema_id}")
        else:
            schema_id = registry.delete_subject(
                args.subject,
            )
    except requests.exceptions.HTTPError as e:
        print(f"Error registering schema: {e}")
        if e.response is not None:
            print(f"Response: {e.response.text}")
        exit(1)


if __name__ == "__main__":
    main()
