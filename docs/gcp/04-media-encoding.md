# GCP Storage Setup - Media Encoding

```shell
gcloud config set project open-broadcast
```

### Create Storage Bucket

```shell
gsutil mb -p open-broadcast -c standard -l europe-west6 -b on gs://obr-master
```


### Storage Triggers

As there is no 'native' support to trigger cloud run by storage events we add a tiny cloud function
to listen to events & trigger the encoding process.

#### File Created (master bucket)

```shell
gcloud functions deploy \
    storage-trigger-master-created \
    --entry-point created \
    --project open-broadcast \
    --runtime python38 \
    --region europe-west6 \
    --source ./functions/storage-trigger/ \
    --timeout 300 \
    --trigger-bucket obr-master
```


### Enccoding (Cloud Run)

