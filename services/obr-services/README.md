# OBR Services

We run a couple of services on the `obr-services` VM. Initially the deployment was planned to be 
fully "serverless", but due to the high costs we run them on a VM for the moment.

## SSH Access

 - IP: `34.65.201.172`

```shell
ssh -t 34.65.201.172 -l $GCP_SSH_USER 'sudo -u obr -i'
```

## Setup & Deployment

```shell
ansible-playbook -i 34.65.201.172, ansible/obr-services.yml
```


## Secrets Access

```shell
gcloud compute instances set-service-account obr-services \
    --zone europe-west6-a \
    --service-account app-core@open-broadcast.iam.gserviceaccount.com \
    --scopes "https://www.googleapis.com/auth/cloud-platform"
```