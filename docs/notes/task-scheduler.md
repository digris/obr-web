

```shell
# pub-sub topic
projects/open-broadcast/topics/ch-openbroadcast-bridge-topic 
```

```shell
# payload
{
  "command": "sync_schedule"
}
```


```shell
curl -X POST \
  -H "Content-Type: application/json" \
  -H "Authorization: Token e81c751013a0667fe43f7ed445e3160320107906" \
  -d '{"command": "sync_schedule"}' \
  https://next.openbroadcast.ch/api/v1/pub-sub-bridge/
```