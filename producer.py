import time
import json
import requests
from kafka import KafkaProducer

TOPIC_NAME = 'iss_location'
KAFKA_SERVER = '127.0.0.1:9092'

producer = KafkaProducer(
    bootstrap_servers='127.0.0.1:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

session = requests.Session()

print("🚀 Producer running...")

while True:
    try:
        response = session.get(
            "https://api.wheretheiss.at/v1/satellites/25544",
            timeout=10
        )
        response.raise_for_status()
        data = response.json()

        payload = {
            "latitude": float(data["latitude"]),
            "longitude": float(data["longitude"]),
            "altitude": float(data["altitude"]),
            "velocity": float(data["velocity"]),
            "timestamp": data["timestamp"]
        }

        # ✅ send WITHOUT flush (better performance)
        future = producer.send(TOPIC_NAME, value=payload)

        try:
            future.get(timeout=5)
            print(f"✅ Sent: {payload}")
        except Exception as e:
            print(f"❌ Kafka send failed: {e}")

        time.sleep(3)

    except requests.exceptions.Timeout:
        print("⚠️ API timeout — retrying in 5 sec...")
        time.sleep(5)

    except Exception as e:
        print(f"⚠️ Minor hiccup: {e}")
        time.sleep(3)