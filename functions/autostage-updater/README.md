# AutoStage Updater

- triggered by pub-sub - topic: on-air-update-in-60s
- sends metadata to autostage metadata-service
- [GCP](https://console.cloud.google.com/run/detail/europe-west6/autostage-updater/observability/metrics?project=open-broadcast)


## Notes

### Status

```shell
# status
curl https://onair.radioapi.io/digrisag/openbroadcast/status.json
```

```shell
# on-air (from response above)
curl https://aimonair.b-cdn.net/digrisag/openbroadcast/onair.json
```

### Ingest


```json
{
    "nowPlaying": {
        "type": "song",
        "status": "playing",
        "time": "2024-06-01T12:00:00Z",
        "title": "Song Title",
        "artist": "Artist Name",
        "duration": 60,
        "imageUrl": "https://example.com/image.jpg"
    }
}
```

```shell
export API_KEY=***
export API_CID=***


# curl post with example payload
curl -X POST \
    -H "Content-Type: application/json" \
    -d '{
        "nowPlaying": {
            "type": "song",
            "status": "playing",
            "time": "2024-06-01T12:00:00Z",
            "title": "Song Title",
            "artist": "Artist Name",
            "duration": 60,
            "imageUrl": "https://example.com/image.jpg"
        }
    }' \
    'https://onair.radioapi.io/ingest/digrisag/openbroadcast?format=radioapi&key=$API_KEY&cid=$API_CID'
```


## Deploy CF

```shell
gcloud functions deploy \
    autostage-updater \
    --entry-point run \
    --project open-broadcast \
    --runtime python312 \
    --gen2 \
    --region europe-west6 \
    --source ./ \
    --trigger-topic on-air-update-in-60s
```

## Run Locally

NOTE: their API is quite crap - they don't validate API_KEY / API_CID ;) ...

```shell
API_KEY=*** \
API_CID=3690 \
./main.py
```