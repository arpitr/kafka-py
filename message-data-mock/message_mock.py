from flask import Flask, jsonify
from datetime import datetime
import time
import random


app = Flask(__name__)

def generate_unique_number():
    timestamp = int(time.time() * 1000)  # Current time in milliseconds
    random_part = random.randint(1000, 9999)  # 4-digit random number
    unique_number = int(f"{timestamp}{random_part}")
    return unique_number

def get_random_user_activity():
    activities = [
        "user logged in.",
        "user logged out.",
        "user updated.",
        "user deleted.",
        "user requested forgot password.",
        "user requested forgot email.",
        "user requested for payment.",
        "user requested for cancellation."
    ]
    return random.choice(activities)

@app.route('/user-activities', methods=['GET'])
def get_activities():
    current_timestamp = int(datetime.now().timestamp() * 1000)
    data = [
        {
            "id": generate_unique_number(),
            "action": get_random_user_activity(), 
            "timestamp": current_timestamp
        },
        {
            "id": generate_unique_number(),
            "action": get_random_user_activity(),
            "timestamp": current_timestamp
        },
        {
            "id": generate_unique_number(),
            "action": get_random_user_activity(),
            "timestamp": current_timestamp
        }
    ]
    return jsonify(data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9999)