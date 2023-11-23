import api_client
import functions_framework
import datetime
import json
import logging

from flask import request

from google.api_core.exceptions import GoogleAPIError
from google.cloud import tasks_v2, pubsub_v1
from google.protobuf import timestamp_pb2

'''
SELF-URL: https://metadata-updater-kcek2ea7xq-oa.a.run.app
'''

PROJECT_ID = "open-broadcast"
LOCATION = "europe-west6"

QUEUE = "metadata-updater"
TOPIC_ID = "metadata-update"

RUN_URL = "https://metadata-updater-kcek2ea7xq-oa.a.run.app?run=1"


client = tasks_v2.CloudTasksClient()
parent = client.queue_path(PROJECT_ID, LOCATION, QUEUE)

publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(PROJECT_ID, TOPIC_ID)


def schedule_next_run(in_seconds):

    dt = datetime.datetime.utcnow() + datetime.timedelta(seconds=in_seconds)

    timestamp = timestamp_pb2.Timestamp()
    timestamp.FromDatetime(dt)

    payload = {
        "parent": parent,
        "task": {
            "http_request": {
                "http_method": tasks_v2.HttpMethod.POST,
                "url": RUN_URL,
            },
            "schedule_time": timestamp,
        },
    }

    print(f"in_seconds: {in_seconds}")
    print(f"timestamp:  {timestamp}")
    print("payload:", payload)

    response = client.create_task(request=payload)

    logging.info("Created task %s", response.name)


@functions_framework.http
def run(request):
    args = request.args
    # print("request:", request)
    # print("args:", args)

    if not args.get("run") == "1":
        return "SKIP"

    try:
        next_start_in, result = api_client.get_metadata()
    except api_client.ApiError as e:
        print(f'ApiError: {e}')
        next_start_in = 60

    data = json.dumps(result).encode("utf-8")

    future = publisher.publish(topic_path, data)
    print(future.result())

    schedule_next_run(in_seconds=next_start_in)
    return "OK"
