#! /bin/bash

gcloud builds submit \
  --tag gcr.io/open-broadcast/media-encoder

gcloud run deploy media-encoder \
  --region=europe-west6 \
  --image gcr.io/open-broadcast/media-encoder \
  --memory 4096M \
  --concurrency 4 \
  --timeout 900 \
  --platform managed \
  --allow-unauthenticated
