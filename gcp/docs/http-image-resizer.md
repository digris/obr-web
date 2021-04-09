## Image Resizer (HTTP) - Cloud Function

```shell
gcloud config set project open-broadcast
```




## Service Account

```shell script
gcloud iam service-accounts create \
  --project open-broadcast \
  image-resizer
```

```shell script
gcloud projects add-iam-policy-binding open-broadcast \
    --member="serviceAccount:image-resizer@open-broadcast.iam.gserviceaccount.com" \
    --role="roles/viewer"

gcloud projects add-iam-policy-binding open-broadcast \
    --member="serviceAccount:image-resizer@open-broadcast.iam.gserviceaccount.com" \
    --role="projects/open-broadcast/roles/ImageResizer"
```


## Cloud Run

```shell script
gcloud services enable \
    --project open-broadcast \
    cloudfunctions.googleapis.com
```

```shell script
gcloud functions deploy \
  image-resizer \
  --entry-point ResizeImage \
  --project open-broadcast \
  --service-account image-resizer@open-broadcast.iam.gserviceaccount.com \
  --runtime go113 \
  --region europe-west6 \
  --source ./functions/http-image-resizer/ \
  --allow-unauthenticated \
  --trigger-http
```
