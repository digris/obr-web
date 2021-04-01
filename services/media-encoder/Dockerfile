FROM python:3.9-slim

ENV PYTHONUNBUFFERED True

RUN set -ex \
    && apt-get update \
    && apt-get install -y \
        ffmpeg

COPY requirements.txt ./

RUN pip install -r requirements.txt

ENV APP_HOME /app
WORKDIR $APP_HOME
COPY . ./

CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 main:app