import asyncio
import websockets
import json
from kafka import KafkaConsumer

async def kafka_to_websocket(websocket):
    print("🌐 Browser connected")

    consumer = None

    try:
        consumer = KafkaConsumer(
            'iss_location',
            bootstrap_servers=['127.0.0.1:9092'],
            value_deserializer=lambda x: json.loads(x.decode('utf-8')),
            api_version=(0, 10, 1),
            auto_offset_reset='latest',
            group_id='web-bridge-group'
        )

        print("🔄 Streaming Kafka → WebSocket")

        while True:
            msg_pack = consumer.poll(timeout_ms=1000)

            for tp, messages in msg_pack.items():
                for message in messages:
                    data = message.value

                    # ✅ clean forward
                    print(f"📡 Forwarding: {data}")

                    await websocket.send(json.dumps(data))

            await asyncio.sleep(0.05)

    except websockets.exceptions.ConnectionClosed:
        print("❌ Browser disconnected")

    except Exception as e:
        print(f"⚠️ Bridge error: {e}")

    finally:
        if consumer:
            consumer.close()
            print("🧹 Kafka consumer closed")


async def main():
    print("🚀 Bridge running on ws://127.0.0.1:8765")

    async with websockets.serve(kafka_to_websocket, "0.0.0.0", 8765):
        await asyncio.Future()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n🛑 Bridge stopped")