# Metadata Updater

### Deploy CF

```shell
gcloud functions deploy \
    metadata-updater \
    --entry-point run \
    --project open-broadcast \
    --runtime python312 \
    --gen2 \
    --region europe-west6 \
    --source ./functions/metadata-updater/ \
    --trigger-http \
    --allow-unauthenticated
```