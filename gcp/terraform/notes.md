## Configure `terraform` 

```shell
# versions.tf
terraform {
  required_providers {
    google = {
      source = "hashicorp/google"
    }
  }
  required_version = ">= 0.13"
}
```

```shell
 terraform init
```


## GCP Service Account

key:

`~/.keys/open-broadcast/gcp-service-account-infrastructure.json`

```shell
gcloud iam service-accounts create infrastructure
gcloud projects add-iam-policy-binding open-broadcast \
  --member="serviceAccount:infrastructure@open-broadcast.iam.gserviceaccount.com" \
  --role="roles/owner"
```

```shell
gcloud iam service-accounts keys create \
  ~/.keys/open-broadcast/gcp-service-account-infrastructure.json \
  --iam-account=infrastructure@open-broadcast.iam.gserviceaccount.com
```

```shell
export GOOGLE_APPLICATION_CREDENTIALS="/Users/ohrstrom/.keys/open-broadcast/gcp-service-account-infrastructure.json"
```