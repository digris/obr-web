# 

## Sync "old" schedule data

NOTE: only needs to be run once to initially populate the DB & media storage.

```shell
# e.g. sync year 2014 ;)
DJANGO_SETTINGS_MODULE=config.settings.sync ./manage.py \
  sync_schedule \
  -s 2014-01-01 \
  -e 2015-01-01 \
  -f
```

## Via API

```shell
curl \
  -X POST \
  -H "Authorization: Token ba8839c8fe539dd512889e4be4cb130f5cedefa8" \
  https://j.pbi.io/api/v1/sync/schedule/
```