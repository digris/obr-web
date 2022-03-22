FROM nginx:1.21

RUN apt-get update && apt-get install -y \
    nginx-extras \
    libnginx-mod-http-headers-more-filter

ADD nginx.conf /etc/nginx/nginx.conf
ADD default.conf.template /etc/nginx/templates/default.conf.template

ENV \
  SERVER_NAME=local.obr-next \
  CORE=host.docker.internal:8080 \
  STATIC=host.docker.internal:3000 \
  IMAGE_RESIZER=image-resizer:8000
