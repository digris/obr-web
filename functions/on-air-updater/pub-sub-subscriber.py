#! /usr/bin/env python3
import json
from concurrent.futures import TimeoutError
from google.cloud import pubsub_v1


PROJECT_ID = "open-broadcast"
SUBSCRIPTION_ID = "on-air-updated"

subscriber = pubsub_v1.SubscriberClient()
subscription_path = subscriber.subscription_path(PROJECT_ID, SUBSCRIPTION_ID)

def callback(message: pubsub_v1.subscriber.message.Message):
    data = json.loads(message.data.decode("utf-8"))
    print(json.dumps(data, indent=2))
    message.ack()

streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)
print(f"listening for messages: {subscription_path}")

with subscriber:
    try:
        streaming_pull_future.result()
    except TimeoutError:
        streaming_pull_future.cancel()
        streaming_pull_future.result()