# FTP Server

At the moment this simple FTP server is used to get news from RSI.

## SSH Access

 - IP: `34.65.11.251`

```shell
gcloud compute ssh --zone "europe-west6-a" "news-ftp" --project "open-broadcast"
# or
ssh -t 34.65.11.251 -l $GCP_SSH_USER 'sudo -u obr -i'
```

## Setup & Deployment

Create N1-micro in `europe-west6-a`

```shell
ansible-playbook -i 34.65.11.251, ansible/news-ftp.yml
```

```shell
gcloud compute firewall-rules create ftp-server \                                                                                                                                                                         obr-web/git/main !+
  --allow tcp:21,tcp:60000-65535 \
  --direction=INGRESS \
  --priority=1000 \
  --network=default \
  --target-tags=ftp-server \
  --description="Allow FTP and passive ports
```