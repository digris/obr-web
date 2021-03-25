#######################################################################
# node based builder to build front end / vue.js
#######################################################################
FROM node:lts-alpine as node-builder

WORKDIR /root/

COPY ["yarn.lock", "package.json", "./"]
RUN set -ex \
    && apk add \
        git \
    && yarn install

ENV NODE_ENV=production

COPY ["babel.config.js", "vue.config.js", ".eslintrc.js", "./"]
ADD ./src/ ./src/
RUN yarn build


#######################################################################
# python base image
#######################################################################
FROM python:3.9-slim as python-base

WORKDIR /root/

ENV PYTHONFAULTHANDLER=1 \
    PYTHONHASHSEED=random \
    PYTHONUNBUFFERED=1

RUN set -ex \
    && apt-get update \
    && apt-get install -y \
        gettext


#######################################################################
# python builder to install poetry & dependencies
#######################################################################
FROM python-base as python-builder

WORKDIR /root/

ENV PIP_DEFAULT_TIMEOUT=100 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1 \
    POETRY_VERSION=1.1.5

RUN pip3 install -U pip "poetry==$POETRY_VERSION" \
    && python -m venv /venv

COPY ["pyproject.toml","poetry.lock", "./"]

# https://stackoverflow.com/questions/53835198/integrating-python-poetry-with-docker
RUN poetry export -f requirements.txt | /venv/bin/pip install -r /dev/stdin

ADD ./core/ ./core/

RUN set -ex \
    && poetry build \
    && /venv/bin/pip install dist/*.whl


#######################################################################
# pfinal container containing compiled front end & back end
#######################################################################
FROM python-base as final


RUN useradd -m -d /app app

WORKDIR /app/

COPY --from=node-builder /root/build/ ./build
COPY --from=python-builder /venv /venv

COPY ["manage.py", "./"]
ADD ./core/ ./core/

ENV PATH="/venv/bin:$PATH"

ENV DJANGO_SETTINGS_MODULE=core.settings.build
RUN ./manage.py check
RUN ./manage.py collectstatic --clear --no-input
#RUN ./manage.py compilemessages
RUN unset DJANGO_SETTINGS_MODULE

USER app

ENV DJANGO_SETTINGS_MODULE=core.settings.gcp \
    PORT=8000

EXPOSE 8000

CMD exec gunicorn core.wsgi --bind :$PORT --workers 2 --timeout 600
