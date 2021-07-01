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
dropdb ch_openbroadcast_next_local
createdb ch_openbroadcast_next_local

psql \
  -d ch_openbroadcast_next_local \
  -f ./data/db/dump.sql
```