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
	npx stylelint "./src/**/*.(scss|js|vue)"
	yarn lint
	black --check ./core/
	poetry run prospector -p ./core/

fix:
	npx stylelint "./src/**/*.(scss|js|vue)" --fix
	yarn fix
	find ./core/ -type f -name "*.py" -exec pyupgrade --py39-plus "{}" \;
	black ./core/

test-be:
	pytest -m "not e2e" -s ./core/tests/

test-e2e:
	pytest -m "e2e" -s ./core/tests/

test-fe:
	yarn test:unit

test:
	make test-be
	make test-fe
	make test-e2e

docker-image:
	docker build --build-arg GIT_SHORT_SHA=$(GIT_SHORT_SHA) -f ./docker/Dockerfile -t $(DOCKER_TAG):latest .

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
	  -l de \
	  -l fr \
	  -x 'core/base/*'
	poetry run ./manage.py compilemessages

run-hypercorn:
	hypercorn core.asgi:application --bind :${PORT} --access-logfile - --error-logfile - --reload