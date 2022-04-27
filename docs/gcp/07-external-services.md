## Configure External (non GCP) Services

### Stream

```shell
gcloud iam service-accounts create stream

gcloud projects add-iam-policy-binding open-broadcast \
    --member="serviceAccount:stream@open-broadcast.iam.gserviceaccount.com" \
    --role="roles/logging.logWriter"

gcloud iam service-accounts keys create \
  tmp-key.json \
  --iam-account=stream@open-broadcast.iam.gserviceaccount.com
```