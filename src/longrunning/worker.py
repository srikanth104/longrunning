import asyncio

from longrunning.task import Task, TaskStatus

class Worker:
    """Execute thas using agent """
    async def process(self, task: Task) -> None:
        """Execute a queued task and update its status."""
        task.status = TaskStatus.RUNNING
        await asyncio.sleep(10)
        task.status = TaskStatus.COMPLETED
        task.result = "Task completed successfully."
        