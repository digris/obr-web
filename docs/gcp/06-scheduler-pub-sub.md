# Pub/Sub Bridge

NOTE: pub-sub-bridge is not in use anymore.
      cloud scheduler can now natively run HTTP requests

CF to route calls to API.

```shell
gcloud pubsub topics create \
  ch-openbroadcast-bridge-topic

gcloud pubsub subscriptions create \
  ch-openbroadcast-bridge-sub \
  --topic ch-openbroadcast-bridge-topic
```

Create schedule:  

https://console.cloud.google.com/cloudscheduler/jobs/new?project=open-broadcast

```shell
# test
gcloud pubsub subscriptions pull \
  ch-openbroadcast-bridge-sub \
  --limit 5

```

### Deploy CF

```shell

gcloud functions deploy \
    ch-openbroadcast-bridge \
    --entry-point bridge \
    --project open-broadcast \
    --runtime python38 \
    --region europe-west6 \
    --source ./functions/pub-sub-bridge/ \
    --trigger-topic ch-openbroadcast-bridge-topic
```
