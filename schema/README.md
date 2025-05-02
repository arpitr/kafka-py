#  Schema Registry


## 🧾 Register User Activity Schema in AVRO
```bash
# Register as key schema instead of value schema
./register_purchase_schema.py --registry-url http://localhost:8081 --subject user-activity-value --key-subject

# Specify a compatibility level
./register_purchase_schema.py --registry-url http://localhost:8081 --topic user-activity-value --compatibility BACKWARD

# Use a different schema file
./register_purchase_schema.py --registry-url http://localhost:8081 --topic user-activity-value --schema-file user_activity_schema.avsc
```

