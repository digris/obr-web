# Geolocation

Assumes respective request headers configured on GCP load-balancer

```shell
gcloud beta compute backend-services update ch-openbroadcast-be \
  --global \
  --custom-request-header 'X-Client-Geo-Location-Region:{client_region}' \
  --custom-request-header 'X-Client-Geo-Location-City:{client_city}' \
  --custom-request-header 'X-Client-Geo-Location-Coordinates:{client_city_lat_long}'
```