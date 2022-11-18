## Login Redirector - Cloud Function

```shell
gcloud config set project open-broadcast
```


## Cloud Functions

```shell
gcloud functions deploy \
  social-auth-redirector \
  --entry-point auth_redirect \
  --project open-broadcast \
  --runtime python310 \
  --region europe-west6 \
  --source ./functions/social-auth-redirector/ \
  --allow-unauthenticated \
  --trigger-http
```
