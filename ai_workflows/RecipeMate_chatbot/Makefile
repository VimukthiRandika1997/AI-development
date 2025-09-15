
### - Local development - ###
# Load environment variables from .env file
ifneq (,$(wildcard ./.env))
    include .env
    export
endif

SHELL := /bin/bash

run-env:
	python3 -m venv env
	pip3 install -r requirements.txt
	source env/bin/activate

# Define the FastAPI run command target
run-backend:
	uvicorn api.app:app --host 0.0.0.0 --port 8080 --reload

# Define the Streamlit run target
run-frontend:
	streamlit run ui/app.py --server.port=8501 --server.address=0.0.0.0

# Define Redis run target
run-redis:
	docker run -d --name redis-local -p 6379:6379 redis:7-alpine

run-reset:
	docker stop redis-local
	docker container prune

# Aggregate command to run backend, frontend, and redis
run-local:
	$(MAKE) run-env
	$(MAKE) run-redis
	$(MAKE) run-backend &
	$(MAKE) run-frontend

run-local-up:
	$(MAKE) run-redis
	$(MAKE) run-backend &
	$(MAKE) run-frontend


### - Docker container based approach - ###
run-build:
	docker compose build --no-cache
	docker compose up

run-up:
	docker-compose up

run-down:
	docker-compose down -v

