# Run Services (non-dev)

Run the application as a whole using docker compse.

This setup is intended to be used for testing & developing 3rd-party
tool - like iOS app, playout, etc.


## Preparation

```shell
mkdir -p data/ data/master/ data/media data/encoded
```


## Initially build images & populate DB 

```shell
export BUILDKIT_PROGRESS=plain 

docker compose build

docker compose up migrate
docker compose run core ./manage.py createsuperuser
```


## Configuration

Create an `.env` file with the following variables:

NOTE: `SITE_URL` has to match your situation when accessing via network.

```env
DEBUG=True
SITE_URL=http://localhost:5000
DJANGO_SETTINGS_MODULE=config.settings.env

OBP_SYNC_ENDPOINT=https://www.openbroadcast.org/api/v2/obr-sync/
OBP_SYNC_TOKEN=<ASK FOR TOKEN!>

# use to override defaults defined in:
# config/settings/base.py
#JWT_TOKEN_LIFETIME=60
#JWT_TOKEN_REFRESH_LIFETIME=300
#CDN_POLICY_LIFETIME=120
#CDN_POLICY_DOMAIN=localhost

IMAGE_RESIZER_ENDPOINT=/images/
GOOGLE_APPLICATION_CREDENTIALS=***
STRIPE_PUBLISHABLE_KEY=***
STRIPE_SECRET_KEY=***

COMPOSE_PROJECT_NAME=obr
```


## Running 

NOTE: in case you have configured `OBP_SYNC_TOKEN` it will take quite 
some time to download and encode the media-files ;) 

```shell
docker compose up
```


## Cleanup

```shell
# reset
docker compose down --rmi local --remove-orphans

# reset, also delete volumes / db / data
docker compose down --rmi local --volumes --remove-orphans
rm -Rf data/*
```
