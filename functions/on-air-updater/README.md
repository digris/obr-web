# On-Air Updater

- reads on-air info
- emits current data to pub-sub - topic: on-air-updated
- schedules itself to run on next item start-time

## Create Task Queue

```shell
gcloud tasks queues create on-air-updater --location=europe-west6
```

## Create Pub-Sub Topic & Subscription

```shell
gcloud pubsub topics create on-air-updated
gcloud pubsub subscriptions create on-air-updated --topic on-air-updated
```

## Prepare Subscription


## Deploy CF

```shell
gcloud functions deploy \
    on-air-updater \
    --entry-point run \
    --project open-broadcast \
    --runtime python312 \
    --gen2 \
    --region europe-west6 \
    --source ./ \
    --trigger-http \
    --allow-unauthenticated
```