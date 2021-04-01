
```shell
gcloud builds submit \
  --tag gcr.io/open-broadcast/media-encoder
```

```shell
# NOTE: eventarc not available in zurich now (2021-03-30)
gcloud run deploy media-encoder \
  --region=europe-west6 \
  --image gcr.io/open-broadcast/media-encoder \
  --platform managed \
  --allow-unauthenticated
```
