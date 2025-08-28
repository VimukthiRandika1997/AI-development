from typing import List, Optional, Protocol
from app.domain.task import Task
from app.models.task_model import TaskModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from datetime import datetime

class TaskRepositoryInterface(Protocol):
    async def add(self, task: Task) -> Task: ...
    async def list_all(self) -> List[Task]: ...
    async def get(self, task_id: int) -> Optional[Task]: ...
    async def update(self, task: Task) -> Task: ...

class SQLAlchemyTaskRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add(self, task: Task) -> Task:
        model = TaskModel(
            title=task.title,
            description=task.description,
            completed=task.completed,
            created_at=task.created_at or datetime.utcnow(),
        )
        self.session.add(model)
        await self.session.flush()
        await self.session.commit()
        await self.session.refresh(model)
        return Task(
            id=model.id,
            title=model.title,
            description=model.description,
            completed=model.completed,
            created_at=model.created_at,
        )

    async def list_all(self) -> List[Task]:
        q = await self.session.execute(select(TaskModel).order_by(TaskModel.id))
        rows = q.scalars().all()
        return [Task(id=r.id, title=r.title, description=r.description, completed=r.completed, created_at=r.created_at) for r in rows]

    async def get(self, task_id: int) -> Optional[Task]:
        q = await self.session.execute(select(TaskModel).where(TaskModel.id == task_id))
        model = q.scalar_one_or_none()
        if not model:
            return None
        return Task(id=model.id, title=model.title, description=model.description, completed=model.completed, created_at=model.created_at)

    async def update(self, task: Task) -> Task:
        q = await self.session.execute(select(TaskModel).where(TaskModel.id == task.id))
        model = q.scalar_one_or_none()
        if not model:
            return None
        if task.title is not None:
            model.title = task.title
        if task.description is not None:
            model.description = task.description
        if task.completed is not None:
            model.completed = task.completed
        await self.session.commit()
        await self.session.refresh(model)
        return Task(id=model.id, title=model.title, description=model.description, completed=model.completed, created_at=model.created_at)
