# FastAPI Clean Architecture (async SQLAlchemy)


This project demonstrates Clean Architecture using FastAPI + async SQLAlchemy.


## Features

- Domain / Application / Infrastructure / Presentation separation
- Async SQLAlchemy (2.0) with AsyncSession
- Dependency injection via FastAPI Depends
- Pydantic schemas for request/response
- Repository pattern with an interface and a concrete DB implementation


## Run locally

```bash
# Make database migrations
bash create_migrations.sh

# Just start containers (DB + web)
make up

# Run migrations only
make migrate

# Destroy containers
make down

# Full reset (drop DB + apply migrations + start app)
make reset
```


See API docs: http://127.0.0.1:8000/docs and interact with the endpoints