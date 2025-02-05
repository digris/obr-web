FROM python:3.12-alpine

ENV PYTHONUNBUFFERED True

RUN pip3 install -U pip uvicorn fastapi pydantic-settings

WORKDIR /app
COPY services/sse-publisher/ ./

EXPOSE 8000

CMD exec uvicorn main:app --host 0.0.0.0 --port 8000
