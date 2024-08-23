# TuneIn Updater

- triggered by pub-sub - topic: on-air-update-in-60s
- sends metadata to QuantumCast "MetaPort"


## Deploy CF

```shell
gcloud functions deploy \
    quantumcast-updater \
    --entry-point run \
    --project open-broadcast \
    --runtime python312 \
    --gen2 \
    --region europe-west6 \
    --source ./ \
    --trigger-topic on-air-update-in-60s
```

## Run Locally

# 108_9sbtyowq5id_9z3d/hgqmLjKkky9c3jKL

```shell
CHANNEL_KEY=108_9sbtyowq5id_9z3d \
API_TOKEN=*** \
./main.py
```