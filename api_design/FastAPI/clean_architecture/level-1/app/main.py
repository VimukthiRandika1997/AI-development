# app/main.py
from fastapi import FastAPI
from app.api.v1 import task_routes

app = FastAPI(title="Clean Architecture Example")

app.include_router(task_routes.router, prefix="/tasks", tags=["tasks"])
