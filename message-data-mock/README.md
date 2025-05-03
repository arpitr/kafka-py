# User Activities API

This is a simple Flask-based API that returns simulated user activity logs. Each log contains a unique ID, a randomly selected user action, and a timestamp.

## 📌 Endpoint

### `GET /user-activities`

Returns a list of three user activity records in JSON format.

#### Example Response

```json
[
  {
    "id": 17147417632451023,
    "action": "user logged out.",
    "timestamp": 1714741763245
  },
  {
    "id": 17147417632458749,
    "action": "user requested for payment.",
    "timestamp": 1714741763245
  },
  {
    "id": 17147417632458231,
    "action": "user updated.",
    "timestamp": 1714741763245
  }
]
