## Copy live DB to local development

NOTE: Assumes using postgres provided via `docker-compose`.

Ensure that (at least) the DB container is up and running:

```shell
docker-compose up db
```

As well as `sql-proxy`

```shell
./bin/sql-proxy
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
dropdb \
  -h 127.0.0.1 \
  -p 5434 \
  -U obr \
  -W \
  -f \
  obr
  
createdb \
  -h 127.0.0.1 \
  -p 5434 \
  -U obr \
  -W \
  obr

psql \
  -h 127.0.0.1 \
  -p 5434 \
  -U obr \
  -W \
  -d obr \
  -f ./data/db/dump.sql
```