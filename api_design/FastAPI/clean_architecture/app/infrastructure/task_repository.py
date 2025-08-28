# app/infrastructure/task_repository.py
from typing import List, Optional
from app.domain.task import Task

class TaskRepository:
    def __init__(self):
        self._tasks: List[Task] = []
        self._id_counter = 1

    def add(self, task: Task) -> Task:
        task.id = self._id_counter
        self._id_counter += 1
        self._tasks.append(task)
        return task

    def list_all(self) -> List[Task]:
        return self._tasks

    def get(self, task_id: int) -> Optional[Task]:
        return next((t for t in self._tasks if t.id == task_id), None)

    def update(self, task: Task) -> Task:
        for i, t in enumerate(self._tasks):
            if t.id == task.id:
                self._tasks[i] = task
                return task
        return task
