# Icecast Updater

- triggered by pub-sub - topic: on-air-updated
- sends metadata to icecast server


## Deploy CF

```shell
gcloud functions deploy \
    icecast-updater \
    --entry-point run \
    --project open-broadcast \
    --runtime python312 \
    --gen2 \
    --region europe-west6 \
    --source ./ \
    --trigger-topic on-air-updated
```