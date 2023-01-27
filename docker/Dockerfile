#######################################################################
# node based builder to build front end / vue.js
#######################################################################
#FROM node:lts-alpine as node-builder
FROM node:16-slim as node-builder

WORKDIR /root/

RUN set -ex \
    && apt-get update \
    && apt-get install -y \
        git

COPY ["yarn.lock", "package.json", "./"]
ADD ./patches/ ./patches/

#ENV NODE_ENV=production

RUN yarn install

ENV NODE_ENV=production

COPY [ \
  "tsconfig.json", \
  "vite.config.ts", \
  "tsconfig.vite-config.json", \
  "tsconfig.app.json", \
  "tsconfig.vitest.json", \
  ".eslintrc.cjs", \
  "./" \
]

ADD ./src/ ./src/

RUN yarn build

# TODO: maybe use webpack to handle assets?
ADD ./src/assets/ ./build/assets/


#######################################################################
# python base image
#######################################################################
FROM python:3.11-slim as python-base
ARG GIT_SHORT_SHA=""
WORKDIR /root/

ENV PYTHONFAULTHANDLER=1 \
    PYTHONHASHSEED=random \
    PYTHONUNBUFFERED=1 \
    GIT_SHORT_SHA=$GIT_SHORT_SHA

RUN set -ex \
    && apt-get update \
    && apt-get install -y \
        gettext \
        git


#######################################################################
# python builder to install poetry & dependencies
#######################################################################
FROM python-base as python-builder

WORKDIR /root/

ENV PIP_DEFAULT_TIMEOUT=100 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1 \
    POETRY_VERSION=1.2.2

RUN set -ex \
    && apt-get update \
    && apt-get install -y \
        build-essential

RUN pip3 install -U pip "poetry==$POETRY_VERSION" \
    && python -m venv /venv

COPY ["pyproject.toml","poetry.lock", "./"]

# https://stackoverflow.com/questions/53835198/integrating-python-poetry-with-docker
# NOTE: --without-hashes is temporary here to allow install pacvkages from git (only pypi supports hashes)
#RUN poetry export \
#    --without-hashes \
#    -f requirements.txt \
#    | /venv/bin/pip install \
#    -r /dev/stdin

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
ADD ./content/ ./content/
COPY CHANGELOG.md ./content/pages/changelog.md

ENV PATH="/venv/bin:$PATH"

ENV DJANGO_SETTINGS_MODULE=core.settings.build
RUN ./manage.py check
RUN ./manage.py collectstatic --clear --no-input
#RUN ./manage.py compilemessages
RUN unset DJANGO_SETTINGS_MODULE

USER app

ENV DJANGO_SETTINGS_MODULE=core.settings.live \
    PORT=8000 \
    TZ="Europe/Zurich"

EXPOSE 8000

#CMD exec gunicorn core.wsgi --bind :$PORT --workers 2 --timeout 600
CMD exec hypercorn core.asgi:application --bind :$PORT
