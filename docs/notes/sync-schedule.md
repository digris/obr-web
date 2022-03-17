# 

## Sync "old" schedule data

NOTE: only needs to be run once to initially populate the DB & media storage.

```shell
# e.g. sync year 2014 ;)
DJANGO_SETTINGS_MODULE=core.settings.sync ./manage.py \
  sync_schedule \
  -s 2014-01-01 \
  -e 2015-01-01 \
  -f
```