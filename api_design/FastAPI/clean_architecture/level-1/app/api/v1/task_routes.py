# app/api/v1/task_routes.py
from fastapi import APIRouter, Depends, HTTPException
from typing import List
from app.application.task_service import TaskService
from app.infrastructure.task_repository import TaskRepository
from app.schemas import TaskCreate, TaskResponse

router = APIRouter()

# Dependency injection (could later use DI frameworks)
repo = TaskRepository()
task_service = TaskService(repo)

@router.post("/", response_model=TaskResponse)
def create_task(task: TaskCreate):
    return task_service.create_task(task.title, task.description)

@router.get("/", response_model=List[TaskResponse])
def list_tasks():
    return task_service.get_tasks()

@router.put("/{task_id}", response_model=TaskResponse)
def complete_task(task_id: int):
    task = task_service.mark_completed(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task
