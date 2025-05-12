# RFI - Radio France Internationale

## Web Consold

 - https://distribution.cloud.rfi.fr/

## Program Grid

### URL-Pattern

```shell
# full
https://aod-rfi.akamaized.net/rfi/distrib/sons/fr/R2505/journal_international_15h00_-_15h10_gmt_20250508_128.mp3

# prefix
/rfi/distrib/sons/fr/R2505/

# filename
journal_international_15h00_-_15h10_gmt_20250508_128.mp3
journal_international_XXhXX_-_XXhXX_gmt_XXXXXXXX_128.mp3
```

### Timing

|  Time | Duration | File Fragment             | Title                          |
|------:|---------:|---------------------------|--------------------------------|
| 00:00 |       10 |15h00_-_15h10_gmt_20250508 | Journal 08/05/2025 00h00 GMT   |
| 15:00 |       10 |15h00_-_15h10_gmt_20250508 | Journal 08/05/2025 15h00 GMT   |

## Liquidsoap

### Run LS Scripts

```shell
eval $(opam env --switch=ls-23)

# mock news server
SSE_PUBLISHER_URL=http://localhost:8009/sse/ \
SSE_PUBLISHER_API_TOKEN=BLA-BLUP \
./news.liq
```

### News Trigger

Trigger news (HTTP)

```shell
curl \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{"duration":60}' \
  http://localhost:8000/news -i
```
