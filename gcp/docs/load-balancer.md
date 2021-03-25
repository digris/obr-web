# just notes / work-log...

### Network Endpoint Groups (NEG)

https://cloud.google.com/load-balancing/docs/negs

```shell script
gcloud compute network-endpoint-groups create ch-openbroadcast-neg \
    --region=europe-west6 \
    --network-endpoint-type=serverless  \
    --cloud-run-service=ch-openbroadcast-next-core
```


### Backend Service

https://cloud.google.com/load-balancing/docs/backend-service

```shell script
gcloud compute backend-services create ch-openbroadcast-be \
    --global
```

```shell script
# connect with NEG
gcloud compute backend-services add-backend ch-openbroadcast-be \
    --global \
    --network-endpoint-group=ch-openbroadcast-neg \
    --network-endpoint-group-region=europe-west6
```

### UI

From here things are configured via web-interface...


### terraformer export GCP state


```shell
brew install terraformer
```



https://github.com/GoogleCloudPlatform/terraformer

```shell
terraformer import google \
  --resources=addresses \
  --regions=europe-west6 \
  --projects=open-broadcast
```

```shell
terraformer import google \
  --resources=globalAddresses,globalForwardingRules,project \
  --projects=open-broadcast
```