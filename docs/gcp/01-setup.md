# GCP Setup

```shell
gcloud config set project open-broadcast
```

## Tooling Configuration & Variables

```shell
PROJECT_ID=$(gcloud config get-value core/project)
PROJECT_NUMBER=$(gcloud projects describe ${PROJECT_ID} --format 'value(projectNumber)')
REGION=europe-west6

COMPUTE_SERVICE_ACCOUNT=${PROJECT_NUMBER}-compute@developer.gserviceaccount.com
CLOUDBUILD_SERVICE_ACCOUNT=${PROJECT_NUMBER}@cloudbuild.gserviceaccount.com

GS_BUCKET_NAME=ch-openbroadcast-media

echo $PROJECT_ID
echo $PROJECT_NUMBER
echo $REGION
echo $COMPUTE_SERVICE_ACCOUNT
echo $CLOUDBUILD_SERVICE_ACCOUNT
echo $GS_BUCKET_NAME
```


## Infrastructure Setup

### APIs

```shell script
gcloud services enable \
    --project open-broadcast \
    run.googleapis.com \
    sql-component.googleapis.com \
    sqladmin.googleapis.com \
    cloudbuild.googleapis.com \
    vpcaccess.googleapis.com \
    secretmanager.googleapis.com \
    cloudresourcemanager.googleapis.com
```

### IAM / Service Accounts

```shell
gcloud iam service-accounts create app-core \
  --project open-broadcast \
  --display-name="app-core"

```shell
# Grant the IAM Service Account User role to the Cloud Build service account on the Cloud Run runtime service account
gcloud iam service-accounts add-iam-policy-binding \
  --project open-broadcast \
  app-core@open-broadcast.iam.gserviceaccount.com \
  --member="serviceAccount:888119763922@cloudbuild.gserviceaccount.com" \
  --role="roles/iam.serviceAccountUser"
```

### Backing Services

#### Database


```shell

# db
gcloud sql instances create open-broadcast-db --project $PROJECT_ID \
  --database-version POSTGRES_13 --tier db-f1-micro --region $REGION

gcloud sql databases create ch-openbroadcast --instance open-broadcast-db

DBPASS="$(cat /dev/urandom | LC_ALL=C tr -dc 'a-zA-Z0-9' | fold -w 30 | head -n 1)"
gcloud sql users create ch-openbroadcast --instance open-broadcast-db --password $DBPASS

```


### App Configuration / Secrets

```shell
echo DATABASE_URL=\"postgres://ch-openbroadcast:${DBPASS}@//cloudsql/${PROJECT_ID}:${REGION}:open-broadcast-db/ch-openbroadcast\" > .env
echo GS_BUCKET_NAME=\"${GS_BUCKET_NAME}\" >> .env
echo SECRET_KEY=\"$(cat /dev/urandom | LC_ALL=C tr -dc 'a-zA-Z0-9' | fold -w 50 | head -n 1)\" >> .env
echo DEBUG=\"True\" >> .env
```

```shell
gcloud secrets create ch-openbroadcast-settings --data-file .env

gcloud secrets add-iam-policy-binding ch-openbroadcast-settings \
  --member serviceAccount:${COMPUTE_SERVICE_ACCOUNT} --role roles/secretmanager.secretAccessor

gcloud secrets add-iam-policy-binding ch-openbroadcast-settings \
  --member serviceAccount:${CLOUDBUILD_SERVICE_ACCOUNT} --role roles/secretmanager.secretAccessor

gcloud projects add-iam-policy-binding ${PROJECT_ID} \
    --member serviceAccount:${CLOUDBUILD_SERVICE_ACCOUNT} --role roles/cloudsql.client
    
    
# superuser password - will be used in initial (django) migration
    
gcloud secrets create ch-openbroadcast-superuser --replication-policy automatic
gcloud secrets add-iam-policy-binding ch-openbroadcast-superuser \
  --member serviceAccount:${CLOUDBUILD_SERVICE_ACCOUNT} --role roles/secretmanager.secretAccessor

```


## GCP Development Service Account

key:

`~/.keys/open-broadcast/gcp-service-account-dev.json`

```shell
gcloud iam service-accounts create development

gcloud projects add-iam-policy-binding open-broadcast \
  --member="serviceAccount:development@open-broadcast.iam.gserviceaccount.com" \
  --role="roles/owner"
```

```shell
gcloud iam service-accounts keys create \
  ~/.keys/open-broadcast/gcp-service-account-dev.json \
  --iam-account=development@open-broadcast.iam.gserviceaccount.com
```