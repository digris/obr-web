#######################################################################
# node based builder to build front-end / vue.js
#######################################################################
#FROM node:lts-alpine AS node-builder
FROM node:20-slim AS node-builder

WORKDIR /root/

RUN set -ex \
    && apt-get update \
    && apt-get install -y \
        git

COPY ["yarn.lock", "package.json", "./"]

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

ADD ./obr_ui/ ./obr_ui/

RUN yarn build

# TODO: maybe use vite to handle these assets?
ADD ./obr_ui/assets/ ./build/assets/


#######################################################################
# python core image
#######################################################################
FROM python:3.11-slim
ARG GIT_SHORT_SHA=""
WORKDIR /root/

ENV PYTHONFAULTHANDLER=1 \
    PYTHONHASHSEED=random \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    GIT_SHORT_SHA=$GIT_SHORT_SHA \
    PIP_DEFAULT_TIMEOUT=100 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1 \
    POETRY_VERSION=2.0.1

RUN set -ex \
    && apt-get update \
    && apt-get install -y \
    gettext \
    git \
    build-essential

RUN pip3 install -U pip "poetry==$POETRY_VERSION" \
    && poetry config virtualenvs.create false

COPY ["pyproject.toml","poetry.lock", "./"]

RUN poetry install --no-root --without dev

RUN useradd -m -d /app app

WORKDIR /app/

# add node static build
COPY --from=node-builder /root/build/ ./build

ADD ./config/ ./config/
ADD ./obr_core/ ./obr_core/

COPY ["manage.py", "./"]
ADD ./config/ ./config/
ADD ./obr_core/ ./obr_core/
ADD ./content/ ./content/
COPY CHANGELOG.md ./content/pages/changelog.md

ENV DJANGO_SETTINGS_MODULE=config.settings.build
RUN ./manage.py check
RUN ./manage.py collectstatic --clear --no-input
#RUN ./manage.py compilemessages
RUN unset DJANGO_SETTINGS_MODULE

USER app

ENV DJANGO_SETTINGS_MODULE=config.settings.live \
    PORT=8000 \
    TZ="Europe/Zurich"

EXPOSE 8000

CMD exec hypercorn config.asgi:application --workers 1 --bind :$PORT
