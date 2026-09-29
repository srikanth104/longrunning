"""
Main application module.

Creates the FastAPI application for our
long-running agent service.
"""
from uuid import uuid4

from fastapi import BackgroundTasks, FastAPI
from longrunning.task import CreateTaskRequest,Task
from longrunning.worker import Worker
from longrunning.task_store import TaskStore

from contextlib import asynccontextmanager
import asyncio

@asynccontextmanager
async def lifespan(app: FastAPI):

    running_tasks = task_store.get_running_tasks()

    for task in running_tasks:
        asyncio.create_task(worker.process(task))
    yield

app = FastAPI(
    title="Long-Running Agent",
    lifespan=lifespan
)


task_store = TaskStore()
worker = Worker(task_store)


@app.get("/health")
async def health_check() -> dict[str, str]:
    """Return the current health status of the service."""
    return {"status": "healthy"}

@app.post("/tasks")
async def create_task( request: CreateTaskRequest,
                      background_tasks: BackgroundTasks) -> Task:
    """Create a new task and return its initial state."""

    task_id = str(uuid4())
    task = Task(task_id=task_id,
                instruction=request.instruction)

    task_store.save(task)

    background_tasks.add_task(
        worker.process, task
    )
    return task

@app.get("/tasks/{task_id}")
async def get_task(task_id: str) -> Task | None:
    """Return the current state of a task."""
    task = task_store.get(task_id)
    return task

async def recover_tasks():
    tasks = task_store.get_running_tasks()

    for task in tasks:
        await worker.process(task)
