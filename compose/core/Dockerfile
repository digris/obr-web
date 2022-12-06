#######################################################################
# python base image
#######################################################################
FROM python:3.11-slim as python-base
ARG GIT_SHORT_SHA=""
WORKDIR /root/

ENV PYTHONFAULTHANDLER=1 \
    PYTHONHASHSEED=random \
    PYTHONDONTWRITEBYTECODE=1 \
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

RUN poetry export --without-hashes -f requirements.txt | /venv/bin/pip install -q -r /dev/stdin

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

COPY --from=python-builder /venv /venv

COPY ["manage.py", "./"]
ADD ./core/ ./core/

# additional entry-points
COPY compose/core/sync-schedule ./

ENV PATH="/venv/bin:$PATH"

USER app

ENV DJANGO_SETTINGS_MODULE=core.settings.development \
    PORT=8000

EXPOSE 8000

CMD exec hypercorn core.asgi:application --bind :$PORT
