based on https://github.com/didil/gcf-go-image-resizer

## run local server (port 7777)

source (local filesystem or GCP storage bucket) is configured via
`SOURCE` environment variable.

```
export SOURCE=fs://../../data/media
```

```shell
go run cmd/server/server.go
```