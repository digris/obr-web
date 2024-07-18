SHELL := bash
.ONESHELL:
.SHELLFLAGS := -eu -o pipefail -c
.DELETE_ON_ERROR:
MAKEFLAGS += --warn-undefined-variables
MAKEFLAGS += --no-builtin-rules

GCP_PROJECT = open-broadcast
DOCKER_TAG = ch-openbroadcast-next
PORT_BE = 8080
PORT_FE = 3000
GIT_SHORT_SHA = $(shell git rev-parse --short HEAD)

.PHONY: lint-be
lint-be:
	poetry run isort obr_core/ --check
	poetry run ./manage.py spectacular --file /dev/null --validate
	poetry run ruff check obr_core/
	poetry run black --check obr_core/

.PHONY: lint-fe
lint-fe:
	yarn lint

.PHONY: format-be
format-be:
	poetry run isort obr_core/
	poetry run ruff check --fix-only obr_core/
	poetry run black obr_core/

.PHONY: format-fe
format-fe:
	yarn fix

.PHONY: lint
lint: lint-be lint-fe

.PHONY: format
format: format-be format-fe

.PHONY: test-be
test-be:
	pytest -m "not e2e" -s obr_core/tests/

.PHONY: test-e2e
test-e2e:
	pytest -m "e2e" -s obr_core/tests/

.PHONY: test-fe
test-fe:
	yarn test:unit

.PHONY: test
test:
	make test-be
	make test-fe
	make test-e2e

.PHONY: openapi-schema
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

.PHONY: docker-build
docker-build:
	docker build --build-arg GIT_SHORT_SHA=$(GIT_SHORT_SHA) -f ./docker/Dockerfile -t $(DOCKER_TAG):latest .

.PHONY: release
release:
	poetry run semantic-release publish

.PHONY: deploy
deploy:
	gcloud builds submit \
	  --project $(GCP_PROJECT) \
	  --config gcp/build-migrate-deploy.yaml \
	  --timeout=1200

.PHONY: update-settings
update-settings:
	gcloud --project $(GCP_PROJECT) \
	  secrets versions add ch-openbroadcast-settings --data-file .env.live

.PHONY: show-settings
show-settings:
	gcloud --project $(GCP_PROJECT) \
	  secrets versions access latest --secret=ch-openbroadcast-settings

.PHONY: translations
translations:
	poetry run ./manage.py makemessages \
	  --no-wrap \
	  -l de \
	  -l fr \
	  -i 'obr_core/base/*' \
	  -i 'node_modules/*'
	poetry run ./manage.py compilemessages

.PHONY: run-be
run-be:
	./manage.py runserver 0.0.0.0:${PORT_BE}

.PHONY: run-fe
run-fe:
	yarn serve --port ${PORT_FE}

.PHONY: run-hypercorn
run-hypercorn:
	hypercorn config.asgi:application --bind :${PORT_BE} --access-logfile - --error-logfile - --reload