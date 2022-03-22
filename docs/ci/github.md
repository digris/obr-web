## GCP Deployment Service Account

 - Service account: `deploy@open-broadcast.iam.gserviceaccount.com`
 
```shell
gcloud iam service-accounts keys create \
  temp-sa-kej.json \
  --iam-account=deploy@open-broadcast.iam.gserviceaccount.com
```