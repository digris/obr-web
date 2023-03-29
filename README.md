# open broadcast - radio

"Next-gen" version of openbroadcast.ch website to be launched in 2022.

[![CI](https://github.com/digris/obr-web/actions/workflows/ci.yaml/badge.svg)](https://github.com/digris/obr-web/actions/workflows/ci.yaml)

- [GitHub Project](https://github.com/digris/obr-web)
- [Project Board](https://github.com/orgs/digris/projects/2)
- [next.openbroadcast.ch](https://next.openbroadcast.ch/)
- [next.openbroadcast.ch/admin/](https://next.openbroadcast.ch/admin/)
- [Gitlab Project](https://gitlab.com/digris/open-broadcast/openbroadcast.ch)


![screen - radio](docs/screens/radio.png?raw=true "Radio")


## Project setup

Application runs on GCP:

| GCP Organisation | digris.ch      |
|------------------|----------------|
| Project ID       | open-broadcast |
| Project No       | 888119763922   |

[GCP project dashboard](https://console.cloud.google.com/home/dashboard?project=open-broadcast)

```shell
gcloud projects describe open-broadcast
```


## Services & Integrations

- [Stripe](https://...)
- [Sentry](https://sentry.io/organizations/obr/projects/obr/?project=5953969)
- [OpenReplay](https://app.openreplay.com/4567/) (inactive, migrated session tracking to sentry)
- [Analytics](https://analytics.google.com/analytics/web/#/p299020254/reports/intelligenthome)

## Documentation

- [GCP](docs/gcp)
- [Development](docs/development)
- [API](docs/api)
