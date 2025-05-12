# News Service (SRF)

## Signaling

![screen - radio](docs/diagrams/system-overview.drawio.svg "System Overview")

## Run LS Scripts

```shell
eval $(opam env --switch=ls-23)

# mock news server
SSE_PUBLISHER_URL=http://localhost:8009/sse/ \
SSE_PUBLISHER_API_TOKEN=BLA-BLUP \
./news.liq
```
