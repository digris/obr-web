# official docker image does not run on ARM.
# so we have to build it...
FROM golang:1.17-alpine as builder

RUN apk --no-cache add --virtual build-dependencies \
    git \
  && mkdir -p /root/gocode \
  && export GOPATH=/root/gocode \
  && go get github.com/mailhog/MailHog

# RUN go get github.com/mailhog/MailHog

FROM alpine:3
RUN adduser -D -u 1000 mailhog

COPY --from=builder /root/gocode/bin/MailHog /usr/local/bin/

USER mailhog

WORKDIR /home/mailhog

ENTRYPOINT ["MailHog"]

EXPOSE 1025 8025