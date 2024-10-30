#! /usr/bin/env python3
import api_client
import functions_framework
import datetime
import json
import time
import logging
import google.cloud.logging

from google.cloud import tasks_v2, pubsub_v1
from google.cloud.logging_v2.handlers import CloudLoggingHandler
from google.protobuf import timestamp_pb2

# "timeshift" in seconds
TIMESHIFT = -60

PROJECT_ID = "open-broadcast"
LOCATION = "europe-west6"
QUEUE = "on-air-updater"
TOPIC_ID = "on-air-update-in-60s"

RUN_URL = "https://europe-west6-open-broadcast.cloudfunctions.net/on-air-updater?run=1"

log_client = google.cloud.logging.Client()
log_handler = CloudLoggingHandler(log_client)
google.cloud.logging.handlers.setup_logging(log_handler)
logging.getLogger().setLevel(logging.DEBUG)

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

    print("payload", payload)

    response = client.create_task(request=payload)

    logging.info("created task %s", response.name)


@functions_framework.http
def run(request):
    args = request.args

    if not args.get("run") == "1":
        return "SKIP"

    try:
        next_run_in, result = api_client.get_metadata(timeshift=TIMESHIFT)

        data = json.dumps(result).encode("utf-8")
        publisher.publish(topic_path, data)

        logging.debug(result)

    except api_client.ApiError as e:
        logging.warning({
            "error": "ApiError",
            "message": str(e),
        })
        next_run_in = 10

    schedule_next_run(in_seconds=next_run_in)

    return f"OK - next run: {next_run_in}"


if __name__ == "__main__":
    while True:
        try:
            next_run_in, result = api_client.get_metadata(timeshift=TIMESHIFT)
        except api_client.ApiError as e:
            print(f"ApiError: {e}")
            next_run_in = 5

        print(f"next run in: {next_run_in}")

        time.sleep(2)

        # time.sleep(next_run_in + 1)
