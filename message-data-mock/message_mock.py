from flask import Flask, jsonify
from datetime import datetime
import time
import random
import pycountry


app = Flask(__name__)

def get_user_id():
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

def get_user_country():
    countries = [country.name for country in pycountry.countries]
    return random.choice(countries)

@app.route('/user-activities', methods=['GET'])
def get_activities():
    current_timestamp = int(datetime.now().timestamp() * 1000)
    data = [
        {
            "id": get_user_id(),
            "action": get_random_user_activity(), 
            "country": get_user_country(),
            "timestamp": current_timestamp
        },
        {
            "id": get_user_id(),
            "action": get_random_user_activity(),
            "country": get_user_country(),
            "timestamp": current_timestamp
        },
        {
            "id": get_user_id(),
            "action": get_random_user_activity(),
            "country": get_user_country(),
            "timestamp": current_timestamp
        }
    ]
    return jsonify(data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9999)