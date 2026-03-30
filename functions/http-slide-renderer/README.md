# Slide Render Service

```shell
yarn dev # ts watch
yarn start
```

```shell
curl http://localhost:7007/slides/render/playlist:AABBCCDD/400x300.jpg
```


## Service Account

```shell script
gcloud iam service-accounts create \
  --project open-broadcast \
  slide-renderer
  
# creates: slide-renderer@open-broadcast.iam.gserviceaccount.com  
```

```shell
gcloud functions deploy \
  slide-renderer \
  --gen2 \
  --project open-broadcast \
  --service-account slide-renderer@open-broadcast.iam.gserviceaccount.com \
  --runtime nodejs24 \
  --region europe-west6 \
  --source ./functions/http-slide-renderer/ \
  --entry-point=render \
  --allow-unauthenticated \
  --memory 1024MB \
  --max-instances=4 \
  --trigger-http

```