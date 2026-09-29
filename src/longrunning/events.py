import asyncio

class EventManager:

    def _init_(self): 
        self._subscribers = dict[str, list[asyncio.Queue]] = {}

    def subscribe(self, task_id:str) -> asyncio.Queue :

        queue = asyncio.Queue()
        self._subscribers.setdefault(task_id, []).append(queue)

        return queue  
    async def publish(self, task_id: str, event: dict) -> None:

        for queue in self._subscribers.get(task_id, []):
            await queue.put(event)
