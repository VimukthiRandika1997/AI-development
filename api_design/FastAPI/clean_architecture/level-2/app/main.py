from fastapi import FastAPI
from app.api.v1 import task_routes
from app.models.task_model import Base
from app.db.session import engine

app = FastAPI(title="Clean Architecture - Async SQLAlchemy")

app.include_router(task_routes.router, prefix="/tasks", tags=["tasks"])

@app.on_event("startup")
async def startup():
    # Create tables if they don't exist. For production, prefer Alembic migrations.
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.get("/")
async def root():
    return {"message": "FastAPI Clean Architecture (async SQLAlchemy)"}
