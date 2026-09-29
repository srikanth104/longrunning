import asyncio

from longrunning.task import Task, TaskStatus
from longrunning.agent import Agent
from longrunning.task_store import TaskStore

class Worker:

    def __init__(self, task_store: TaskStore) -> None:
        self.task_store = task_store
    """Execute thas using agent """

    async def process(self, task: Task) -> None:
        """Execute a queued task and update its status."""
        task.status = TaskStatus.RUNNING
        self.task_store.save(task)
        agent = Agent(self.task_store)
        result = await agent.execute(task)
        task.status = TaskStatus.COMPLETED
        task.result = result
        self.task_store.save(task)
        task.result = result
        