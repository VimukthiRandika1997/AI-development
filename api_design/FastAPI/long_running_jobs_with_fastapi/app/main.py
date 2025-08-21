# FastAPI entrypoint
from fastapi import FastAPI
from app.api.v1.router import router
from app.db.models import Base
from sqlalchemy import create_engine
from app.core.config import settings

app = FastAPI(title=settings.PROJECT_NAME)

# DB Init
engine = create_engine(settings.DATABASE_URL, connect_args={"check_same_thread": False})
Base.metadata.create_all(bind=engine)

# API
app.include_router(router, prefix="/api/v1")
