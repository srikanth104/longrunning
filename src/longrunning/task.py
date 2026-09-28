from dataclasses import dataclass
from enum import Enum

class TaskStatus(str, Enum):
    QUEUED = "QUEUED"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"

@dataclass
class Task:
     """Represents one execution of an agent."""

     task_id: str
     status: TaskStatus = TaskStatus.QUEUED
     result: str | None = None
