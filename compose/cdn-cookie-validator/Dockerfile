FROM python:3.12-alpine

ENV PYTHONUNBUFFERED True

RUN pip3 install -U pip gunicorn pytz

WORKDIR /app
COPY compose/cdn-cookie-validator/ ./

EXPOSE 8000

CMD exec gunicorn -w 4 main:app --bind :8000
