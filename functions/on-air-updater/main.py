#! /usr/bin/env python3
import api_client
import functions_framework
import datetime
import json
import time
import logging
import google.cloud.logging

from flask import request

from google.api_core.exceptions import GoogleAPIError
from google.cloud import tasks_v2, pubsub_v1
from google.cloud.logging_v2.handlers import CloudLoggingHandler
from google.protobuf import timestamp_pb2

PROJECT_ID = "open-broadcast"
LOCATION = "europe-west6"
QUEUE = "on-air-updater"
TOPIC_ID = "on-air-updated"

RUN_URL = "https://europe-west6-open-broadcast.cloudfunctions.net/on-air-updater?run=1"

log_client = google.cloud.logging.Client()
log_handler = CloudLoggingHandler(log_client)
google.cloud.logging.handlers.setup_logging(log_handler)
logging.getLogger().setLevel(logging.DEBUG)
# log_client.setup_logging()

client = tasks_v2.CloudTasksClient()
parent = client.queue_path(PROJECT_ID, LOCATION, QUEUE)

publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(PROJECT_ID, TOPIC_ID)


def delete_existing_tasks():
    tasks = list(client.list_tasks(request={"parent": parent}))
    print(f"num. existing tasks: {len(tasks)}")

    for task in tasks:
        client.delete_task(request={"name": task.name})
        print("deleted task: {}".format(task.name))


def schedule_next_run(in_seconds):

    logging.debug({
        "in_seconds": in_seconds,
    })

    delete_existing_tasks()

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

    response = client.create_task(request=payload)

    logging.info("created task %s", response.name)


@functions_framework.http
def run(request):
    args = request.args

    if not args.get("run") == "1":
        return "SKIP"

    try:
        next_start_in, result = api_client.get_metadata()

        data = json.dumps(result).encode("utf-8")
        publisher.publish(topic_path, data)

        logging.debug(result)

    except api_client.ApiError as e:
        # print(f"ApiError: {e}")
        logging.warning({
            "error": "ApiError",
            "message": str(e),
        })
        next_start_in = 5

    schedule_next_run(in_seconds=next_start_in)

    return "OK"


if __name__ == "__main__":
    while True:
        try:
            next_start_in, result = api_client.get_metadata()
        except api_client.ApiError as e:
            print(f"ApiError: {e}")
            next_start_in = 5

        logging.debug({
            "next_start_in": next_start_in,
        })

        time.sleep(next_start_in + 1)
