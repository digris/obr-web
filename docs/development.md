# Development

### Prerequisites

 - Python
 - Node

See `package.json` and `pyproject.toml` for version details.

 - [Poetry](https://python-poetry.org/)
 - [Yarn](https://yarnpkg.com/)

### Dependencies

```shell
# install python packages
# in case using pyenv
pyenv install 3.9.7

poetry env use python3.9
poetry install

# install npm mackages
# in case using pyenv
nvm use v14.18.0

yarn install
```


### Settings

Copy and adjust (Django) development settings:

```shell
cp core/settings/example_local_development.py cp core/settings/local_development.py
```

```shell
# Configure ENV variables
export DJANGO_SETTINGS_MODULE=core.settings.local_development
export GOOGLE_APPLICATION_CREDENTIALS=/home/...
```

## Copy live DB to local development

### SQL Proxy

```shell
./bin/sql_proxy
```

```shell
pg_dump \
  -h 127.0.0.1 \
  -p 5433 \
  -U ch-openbroadcast \
  -W \
  ch-openbroadcast \
  --no-acl \
  -f ./data/db/dump.sql
```


```shell
dropdb ch-openbroadcast-local
createdb ch-openbroadcast-local

psql \
  -d ch-openbroadcast-local \
  -f ./data/db/dump.sql
```