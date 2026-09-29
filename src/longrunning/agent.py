import asyncio

from longrunning.task import Task
from longrunning.task_store import TaskStore

class Agent:

    def __init__(self, task_store: TaskStore) -> None:
        self.task_store = task_store

    async def execute(self, task : Task) -> str:

        if task.checkpoint < 1:
        # Step 1
            task.checkpoint = 1
            self.task_store.save(task)

            await asyncio.sleep(5)

        if task.checkpoint < 2:
        # Step 2
            task.checkpoint = 2
            self.task_store.save(task)

            await asyncio.sleep(5)

        if task.checkpoint < 3:
        # Step 3
            task.checkpoint = 3
            self.task_store.save(task)

        return f"Agent completed :{task.instruction} successfully."