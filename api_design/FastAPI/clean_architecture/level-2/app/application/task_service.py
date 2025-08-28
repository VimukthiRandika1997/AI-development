from typing import List, Optional
from app.domain.task import Task
from app.infrastructure.task_repository import TaskRepositoryInterface

class TaskService:
    def __init__(self, repo: TaskRepositoryInterface):
        self.repo = repo

    async def create_task(self, title: str, description: str) -> Task:
        task = Task(id=None, title=title, description=description)
        return await self.repo.add(task)

    async def get_tasks(self) -> List[Task]:
        return await self.repo.list_all()

    async def get_task(self, task_id: int) -> Optional[Task]:
        return await self.repo.get(task_id)

    async def update_task(self, task_id: int, title: Optional[str], description: Optional[str], completed: Optional[bool]) -> Optional[Task]:
        existing = await self.repo.get(task_id)
        if not existing:
            return None
        if title is not None:
            existing.title = title
        if description is not None:
            existing.description = description
        if completed is not None:
            existing.completed = completed
        return await self.repo.update(existing)
