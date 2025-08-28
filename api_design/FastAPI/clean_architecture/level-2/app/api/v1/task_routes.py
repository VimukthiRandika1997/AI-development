from fastapi import APIRouter, Depends, HTTPException
from typing import List
from app.schemas import TaskCreate, TaskResponse, TaskUpdate
from app.application.task_service import TaskService
from app.infrastructure.task_repository import SQLAlchemyTaskRepository
from app.db.session import get_session
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()

async def get_task_service(session: AsyncSession = Depends(get_session)) -> TaskService:
    repo = SQLAlchemyTaskRepository(session)
    return TaskService(repo)

@router.post("/", response_model=TaskResponse, status_code=201)
async def create_task(payload: TaskCreate, svc: TaskService = Depends(get_task_service)):
    return await svc.create_task(payload.title, payload.description)

@router.get("/", response_model=List[TaskResponse])
async def list_tasks(svc: TaskService = Depends(get_task_service)):
    return await svc.get_tasks()

@router.get("/{task_id}", response_model=TaskResponse)
async def get_task(task_id: int, svc: TaskService = Depends(get_task_service)):
    t = await svc.get_task(task_id)
    if not t:
        raise HTTPException(status_code=404, detail="Task not found")
    return t

@router.patch("/{task_id}", response_model=TaskResponse)
async def update_task(task_id: int, payload: TaskUpdate, svc: TaskService = Depends(get_task_service)):
    t = await svc.update_task(task_id, payload.title, payload.description, payload.completed)
    if not t:
        raise HTTPException(status_code=404, detail="Task not found")
    return t