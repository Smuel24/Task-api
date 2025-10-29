from dataclasses import dataclass
from datetime import datetime
from enum import Enum

class TaskStatus(str, Enum):
    PENDING = "pending"
    DONE = "done"

@dataclass
class Task:
    id: int
    title: str
    status: TaskStatus
    created_at: datetime