.PHONY: help build run-dev cli test requirements migration migrate-dev
.DEFAULT_GOAL := help

help:				## Prints help message
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'



build:			    ## Run all services in development environment
	docker-compose -f docker-compose.yml build
run-dev:			## Run all services in development environment
	docker-compose -f docker-compose.yml up

pytest:				## Runs pytest inside container
	docker-compose -f docker-compose.yml run --rm --entrypoint pytest api /app/test
cli:				## Opens CLI inside container
	docker-compose -f docker-compose.yml run --rm --entrypoint /bin/bash api
new-migration:		## Creates new migration file
	docker-compose -f docker-compose.yml run --rm --entrypoint alembic api revision

migrate-dev:		## Migrates database to 'HEAD'
	docker-compose -f docker-compose.yml run --rm --entrypoint alembic api upgrade head

requirements:		## Compiles requirements
	docker-compose -f docker-compose.yml run --rm --entrypoint poetry api export -f requirements.txt --output requirements.txt
