SHELL := bash
.ONESHELL:
.SHELLFLAGS := -eu -o pipefail -c
.DELETE_ON_ERROR:
MAKEFLAGS += --warn-undefined-variables
MAKEFLAGS += --no-builtin-rules

GCP_PROJECT = open-broadcast
DOCKER_TAG = ch-openbroadcast-next
PORT = 8080
GIT_SHORT_SHA = $(shell git rev-parse --short HEAD)

lint:
	yarn lint
	poetry run isort obr_core/ --check
	poetry run ./manage.py spectacular --file /dev/null --validate
	poetry run ruff check obr_core/
	poetry run black --check obr_core/

fix:
	yarn fix
	poetry run isort obr_core/
	poetry run ruff check --fix-only obr_core/
	poetry run black obr_core/

test-be:
	pytest -m "not e2e" -s obr_core/tests/

test-e2e:
	pytest -m "e2e" -s obr_core/tests/

test-fe:
	yarn test:unit

test:
	make test-be
	make test-fe
	make test-e2e

openapi-schema:
	mkdir -p schema
	./manage.py spectacular --validate --fail-on-warn --format openapi-json --file schema.json
	npx openapi -i schema.json -o obr_ui/typings/api/ --exportCore false --exportServices false --indent 2
	rm -f schema.json

.PHONY: setup
setup:
	poetry install
	yarn install

.PHONY: clean
clean:
	rm -Rf dist/*
	rm -Rf build/*

.PHONY: build
build:
	yarn build
	cp -R obr_ui/assets/ build/assets/
	./manage.py collectstatic --no-input

docker-image:
	docker build --build-arg GIT_SHORT_SHA=$(GIT_SHORT_SHA) -f ./docker/Dockerfile -t $(DOCKER_TAG):latest .

release:
	poetry run semantic-release publish

deploy:
	gcloud builds submit \
	  --project $(GCP_PROJECT) \
	  --config gcp/build-migrate-deploy.yaml \
	  --timeout=1200

update-settings:
	gcloud --project $(GCP_PROJECT) \
	  secrets versions add ch-openbroadcast-settings --data-file .env.live

show-settings:
	gcloud --project $(GCP_PROJECT) \
	  secrets versions access latest --secret=ch-openbroadcast-settings

translations:
	poetry run ./manage.py makemessages \
	  --no-wrap \
	  -l de \
	  -l fr \
	  -i 'obr_core/base/*' \
	  -i 'node_modules/*'
	poetry run ./manage.py compilemessages

run-hypercorn:
	hypercorn core.asgi:application --bind :${PORT} --access-logfile - --error-logfile - --reload