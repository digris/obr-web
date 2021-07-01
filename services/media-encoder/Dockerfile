FROM python:3.9-alpine

ENV PYTHONUNBUFFERED True

RUN set -ex \
    && apk add --no-cache \
    ffmpeg \
    bash \
    py3-google-auth \
    build-base \
    libffi-dev \
    linux-headers \
    make \
    g++

COPY requirements.txt ./

RUN pip install -r requirements.txt

ENV APP_HOME /app
WORKDIR $APP_HOME
COPY . ./

CMD exec gunicorn --bind :$PORT --log-level warning --workers 1 --threads 8 --timeout 0 main:app