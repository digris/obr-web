#! /bin/bash

gcloud builds submit \
  --tag gcr.io/open-broadcast/media-encoder

gcloud run deploy media-encoder \
  --region=europe-west6 \
  --image gcr.io/open-broadcast/media-encoder \
  --platform managed \
  --allow-unauthenticated
