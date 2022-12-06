# Development


## Project Setup

### Repository

```shell
git clone git@github.com:digris/obr-web.git
cd obr-web
```


### Prerequisites

 - Python
 - Node
 - Docker

See `package.json` and `pyproject.toml` for version details.

 - [Poetry](https://python-poetry.org/)
 - [Yarn](https://yarnpkg.com/)


### Dependencies

```shell
# install python packages
# using pyenv:
pyenv install 3.11.0

poetry env use python3.11
poetry install

# install npm packages
# using nvm & yarn:
nvm use v18.12.1
yarn install
```


### (Django) Settings

All usual settings can be configured through environment variables.  
To use an `.env` file for configuration:

```shell
# copy and adjust:
cp .env.example .env
```

In order to use the variables defined in `.env` set `DJANGO_SETTINGS_MODULE` to `core.settings.env`.  

For more in-depth changes on the settings module extend `settings.development`.


### `docker-compose` Settings

`docker-compose.yml` also makes use of variables defined in environment / `.env`.  
If needed create a `docker-compose.override.yml` file in order to override the defaults.


## Backing Services

To simplify the development there is a `docker-compose` configuration to run the needed auxiliary services:

| service        | exp. port(s)   |                                 - |
|----------------|---------------:|-----------------------------------|
| nginx          |           5000 | http://local.obr-next:5000/       |
| db             |           5434 | psql://obr:obr@127.0.0.1:5434/obr |
| image-resizer  |              - |                                   |
| media-encoder  |              - |                                   |
| sync-schedule  |              - |                                   |
| mailhog        |     1025, 5025 | http://localhost:5025/            |


### Nginx Service

NOTE: `local.obr-next` should resolve to `localhost` / `127.0.0.1` - so e.g. add it to `/etc/hosts`.

The Nginx service acts as a main entry point & reverse proxy during development:  
http://local.obr-next:5000/

See `compose/nginx/default.conf.template` as a reference.

NOTE: Nginx and the other backing services use the (bind-)mounted `./data/` directory.

---

#### Image Resizer

 * `/images/`

Reverse proxy to `image-resizer` service.

See `functions/http-image-resizer/`.

 - env:     `IMAGE_RESIZER`  
   default: `image-resizer:8000`
 
---
   
#### Encoded Media

 * `/encoded/`
 
Serves (DASH-)encoded media files from mounted `data/encoded/`.

---

#### Compiled Front-End

 * `/static/`
 
Reverse proxy to front-end APP.

Tries first to proxy requests to the Vue.js development server running
on `localhost:3000`.  
In case of failure (502) tries to serve from file, looking in: `dist/`.

 - env:     `STATIC`  
   default: `host.docker.internal:3000`

Intention here is to seamlessly serve (hot-reloading) when running:  
```shell
yarn serve
``` 
and else allow using compiled front-end code from:  
```shell
yarn build && \
  ./manage.py collectstatic
``` 

---

#### Back-End

 * `/`

Reverse proxy to back-end / "core" APP.

 - env:     `CORE`  
   default: `host.docker.internal:8080`
 


## Run Services

### Backing Services - dockerized

NOTE: Assuming you provide a valid `OBP_SYNC_TOKEN` this will start
fetching the schedule data for the current date / day, and also 
encodes all synced media to DASH & HLS. This could take a while...

```shell
# ensure data directories exist
mkdir -p data/media && \
mkdir data/master && \
mkdir data/encoded
```

```shell
docker compose build
docker compose up
```

### Run Core & Front-end - locally

#### Assuming `ENV`, python `PATH` & `DJANGO_SETTINGS_MODULE` configured 

```shell
# core
./manage.py runserver 0.0.0.0:8080
# front-end
yarn serve
```

#### Assuming default setup

```shell
# core
DJANGO_SETTINGS_MODULE=core.settings.env \
poetry run ./manage.py runserver 0.0.0.0:8080
# front-end
yarn serve
```
