# TuneIn Updater

- triggered by pub-sub - topic: on-air-update-in-60s
- sends metadata to tunein


## Deploy CF

```shell
gcloud functions deploy \
    tunein-updater \
    --entry-point run \
    --project open-broadcast \
    --runtime python312 \
    --gen2 \
    --region europe-west6 \
    --source ./ \
    --trigger-topic on-air-update-in-60s
```

## Run Locally

```shell
PARTNER_ID=NxpdyOwG \
PARTNER_KEY=*** \
STATION_ID=s129700 \
./main.py
```