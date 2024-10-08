# On-Air Updater

- reads on-air info
- emits item data to pub-sub - topic: on-air-update-in-60s
- schedules itself to run on next item start-time (taking into account 60s "timeshift")

## Create Task Queue

```shell
gcloud tasks queues create on-air-updater --location=europe-west6
```

## Create Pub-Sub Topic & Subscription

```shell
gcloud pubsub topics create on-air-update-in-60s
gcloud pubsub subscriptions create on-air-update-in-60s --topic on-air-update-in-60s
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