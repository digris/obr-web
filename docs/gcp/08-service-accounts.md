## Core Service Custom SA

```shell
gcloud projects add-iam-policy-binding \
  open-broadcast \
  --member serviceAccount:app-core@open-broadcast.iam.gserviceaccount.com \
  --role roles/cloudsql.client \
  --role roles/storage.objectCreator \
  --role roles/storage.objectViewer \
  --role projects/open-broadcast/roles/AppCore
  
gcloud secrets add-iam-policy-binding \
  ch-openbroadcast-settings \
  --member serviceAccount:app-core@open-broadcast.iam.gserviceaccount.com \
  --role roles/secretmanager.secretAccessor
```

```shell
gcloud run services update \
  ch-openbroadcast-next-core \
  --region europe-west6 \
  --service-account app-core@open-broadcast.iam.gserviceaccount.com
```
