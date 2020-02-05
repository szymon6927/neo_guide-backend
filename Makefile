update-deps:
	pip install pip-tools
	pip-compile --generate-hashes requirements/dev.in --output-file requirements/dev.txt
	pip-compile --generate-hashes requirements/requirements.in --output-file requirements/requirements.txt

format:
	black neo_guide

build:
	@docker-compose -f docker-compose-local.yml up --force-recreate --build

up:
	@docker-compose -f docker-compose-local.yml up

db:
	@docker-compose -f docker-compose-local.yml up -d db

s3:
	@docker-compose -f docker-compose-local.yml up -d localstack
