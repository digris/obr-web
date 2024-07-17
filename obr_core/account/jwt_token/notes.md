
```shell
export ACCOUNT_URL=http://local.obr-next:8080/api/v1/account/users/me/
export REFRESH_URL=http://local.obr-next:8080/api/v1/jwt/refresh/

export TOKEN=***
```


```shell
# /me/
curl -H "Authorization: Bearer ${TOKEN}" ${ACCOUNT_URL} | jq

# /jwt/refresh/
curl -X POST -H "Content-Type: application/json" -d "{\"token\":\"${TOKEN}\"}" ${REFRESH_URL} | jq
```