"""
Main application module.

Creates the FastAPI application for our
long-running agent service.
"""
from uuid import uuid4
from fastapi import BackgroundTasks, FastAPI
from longrunning.task import Task
from longrunning.worker import Worker


app = FastAPI(
    title="Long-Running Agent",
)

tasks: dict[str, Task] = {}

worker = Worker()

@app.get("/health")
async def health_check() -> dict[str, str]:
    """Return the current health status of the service."""
    return {"status": "healthy"}

@app.post("/tasks")
async def create_task( background_tasks: BackgroundTasks) -> Task:
    """Create a new task and return its initial state."""

    task_id = str(uuid4())
    task = Task(task_id=task_id)
    tasks[task_id] = task

    background_tasks.add_task(
        worker.process, task
    )
    return task

@app.get("/tasks/{task_id}")
async def get_task(task_id: str) -> Task:
    """Return the current state of a task."""

    return tasks[task_id]