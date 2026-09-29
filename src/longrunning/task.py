from dataclasses import dataclass
from enum import Enum
from pydantic import BaseModel

class TaskStatus(str, Enum):
    QUEUED = "QUEUED"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"

@dataclass
class Task:
     """Represents one execution of an agent."""

     task_id: str
     instruction: str
     status: TaskStatus = TaskStatus.QUEUED
     result: str | None = None
     checkpoint: int = 0


class CreateTaskRequest(BaseModel):
    instruction: str