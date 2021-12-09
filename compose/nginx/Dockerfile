FROM nginx:1.21

ADD nginx.conf /etc/nginx/nginx.conf
ADD default.conf.template /etc/nginx/templates/default.conf.template

ENV \
  SERVER_NAME=local.obr-next \
  CORE=host.docker.internal:8080 \
  STATIC=host.docker.internal:3000 \
  IMAGE_RESIZER=image-resizer:8000
