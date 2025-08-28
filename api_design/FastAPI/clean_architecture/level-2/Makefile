# Makefile for FastAPI + Postgres + Alembic with wait-for-db

.PHONY: up down rebuild migrate reset

# Start containers (db + web)
up:
	docker-compose up --build -d

# Stop containers
down:
	docker-compose down

# Rebuild containers
rebuild:
	docker-compose up --build -d

# Run migrations (wait-for-db is handled in docker-compose)
migrate:
	docker-compose run --rm alembic

# Reset DB completely: drop volume, rebuild, run migrations, start web
reset:
	@echo "Stopping containers..."
	docker-compose down
	@echo "Removing Postgres volume..."
	docker volume rm level-2_db_data || true
	@echo "Building containers..."
	docker-compose up --build -d db
	@echo "Running migrations..."
	docker-compose run --rm alembic
	@echo "Starting FastAPI web server..."
	docker-compose up -d web
