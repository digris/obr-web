FROM golang:1.16.5 as builder
ENV GOOS linux
ENV CGO_ENABLED 0
WORKDIR /app
COPY functions/http-image-resizer/go.mod functions/http-image-resizer/go.sum ./
RUN go mod download
COPY functions/http-image-resizer/ .
RUN go build cmd/serve.go

FROM alpine:3.14 as production
RUN apk add --no-cache ca-certificates
COPY --from=builder app .
EXPOSE 8000
CMD ./serve
