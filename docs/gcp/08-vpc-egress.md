# Static egress IP

```shell
gcloud compute networks list
```

```shell
gcloud compute networks subnets create \
  sn-services \
  --range=10.124.0.0/28 \
  --network=default \
  --region=europe-west6
```

```shell
gcloud compute networks vpc-access connectors create conector-services \
  --region=europe-west6 \
  --subnet-project=open-broadcast \
  --subnet=sn-services
```

```shell
gcloud compute routers create router-services \
  --network=default \
  --region=europe-west6
```

```shell
gcloud compute addresses create ip-vpc-services \
  --region=europe-west6
```

```shell
gcloud compute routers nats create nat-services \
  --router=router-services \
  --region=europe-west6 \
  --nat-custom-subnet-ip-ranges=sn-services \
  --nat-external-ip-pool=ip-vpc-services
```

```shell
gcloud compute addresses describe ip-vpc-services
```
