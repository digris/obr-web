GCP_PROJECT = open-broadcast
DOCKER_TAG = ch-openbroadcast-next
PORT = 8080

run:
	poetry run ./manage.py runserver 0.0.0.0:$(PORT)

shell:
	poetry run ./manage.py shell

lint:
	yarn lint
	black --check ./core/
	poetry run prospector -p ./core/

fix:
	yarn fix
	black ./core/

build-docker:
	docker build -f ./docker/Dockerfile -t $(DOCKER_TAG):latest .

deploy:
	gcloud builds submit --project $(GCP_PROJECT)

update-settings:
	gcloud --project $(GCP_PROJECT) \
	  secrets versions add ch-openbroadcast-settings --data-file .env

translations:
	poetry run ./manage.py makemessages \
	  -l de \
	  -l fr \
	  -i 'core/base/*'
	poetry run ./manage.py compilemessages
