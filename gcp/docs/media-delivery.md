# GCP Storage Setup - Media Delivery

```shell
gcloud config set project open-broadcast
```

### Create Storage Bucket

```shell
gsutil mb -p open-broadcast -c standard -l europe-west6 -b on gs://obr-media
```

### Load Balancer Setup

```shell
gcloud compute addresses create obr-media-ip \
    --network-tier=PREMIUM \
    --ip-version=IPV4 \
    --global

gcloud compute addresses describe obr-media-ip \
    --format="get(address)" \
    --global

gcloud compute backend-buckets create obr-media-backend-bucket \
    --gcs-bucket-name=obr-media \
    --enable-cdn

gcloud compute url-maps create http-lb \
    --default-backend-bucket=obr-media-backend-bucket

gcloud compute target-http-proxies create http-lb-proxy \
    --url-map=http-lb
    
gcloud compute target-https-proxies create https-lb-proxy \
    --ssl-certificates=https-lb-proxy-cert \
    --url-map=http-lb

gcloud compute forwarding-rules create http-lb-forwarding-rule \
    --address=obr-media-ip \
    --global \
    --target-http-proxy=http-lb-proxy \
    --ports=80

gcloud compute forwarding-rules create https-lb-forwarding-rule \
    --address=obr-media-ip \
    --global \
    --target-https-proxy=https-lb-proxy \
    --ports=443


```


### Key Setup (Signed Cookies)

```shell

head -c 16 /dev/urandom | base64 | tr +/ -_ > cdn.key

gcloud compute backend-buckets \
   add-signed-url-key obr-media-backend-bucket \
   --key-name cdn-key \
   --key-file cdn.key


gsutil iam ch \
  serviceAccount:service-888119763922@cloud-cdn-fill.iam.gserviceaccount.com:objectViewer \
  gs://obr-media

```


### CORS / Header Configuration

```shell
# cors
gsutil cors set cors.json gs://obr-media
```


```shell
gcloud beta compute backend-buckets update obr-media-backend-bucket \
    --custom-response-header='Access-Control-Allow-Credentials: true'
```





### Testing / Debug


```shell
gcloud compute backend-buckets describe obr-media-backend-bucket
```

```shell
# cookie check

curl \
  -b 'Cloud-CDN-Cookie=URLPrefix=aHR0cDovL21lZGlhLm9ici1uZXh0LmhhemVsZmlyZS5jb20vZW5jb2RlZA==:Expires=1616446849:KeyName=cdn-key:Signature=BPmnfRLIN4jM_UCdSyXyEhXC7Yk=' \
  https://media.next.openbroadcast.ch/encoded/F001/manifest.mpd

```


```shell
# invalidate cache
gcloud compute url-maps invalidate-cdn-cache http-lb \
  --path "/encoded/*"
```