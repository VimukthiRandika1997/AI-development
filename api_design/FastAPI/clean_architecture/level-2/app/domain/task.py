from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class Task:
    id: Optional[int]
    title: str
    description: str
    completed: bool = False
    created_at: datetime = datetime.utcnow()