# app/application/task_service.py
from typing import List
from app.domain.task import Task
from app.infrastructure.task_repository import TaskRepository

class TaskService:
    def __init__(self, repo: TaskRepository):
        self.repo = repo

    def create_task(self, title: str, description: str) -> Task:
        task = Task(id=None, title=title, description=description)
        return self.repo.add(task)

    def get_tasks(self) -> List[Task]:
        return self.repo.list_all()

    def mark_completed(self, task_id: int) -> Task:
        task = self.repo.get(task_id)
        task.completed = True
        return self.repo.update(task)
