FROM python:3.9-alpine

ENV PYTHONUNBUFFERED True

RUN set -ex \
    && apk add --no-cache \
    ffmpeg

ENV APP_HOME /app
WORKDIR $APP_HOME
COPY docker/media-encoder/ ./
COPY services/media-encoder/encoder.py ./

CMD exec python main.py /data/master /data/encoded --interval 60