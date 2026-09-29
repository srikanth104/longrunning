import sqlite3

from longrunning.task import Task, TaskStatus


class TaskStore:

    def __init__(self) -> None:
        self._connection = sqlite3.connect("tasks.db")
        self._create_table()

    def _create_table(self) -> None:
        self._connection.execute(
            """
            CREATE TABLE IF NOT EXISTS tasks (
                task_id TEXT PRIMARY KEY,
                instruction TEXT NOT NULL,
                status TEXT NOT NULL,
                result TEXT,
                checkpoint INTEGER NOT NULL DEFAULT 0
            )
            """
        )

        self._connection.commit()

    def save(self, task: Task) -> None:
        self._connection.execute(
            """
            INSERT OR REPLACE INTO tasks
            (task_id, instruction, status, result, checkpoint)
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                task.task_id,
                task.instruction,
                task.status.value,
                task.result,
                task.checkpoint
            ),
        )

        self._connection.commit()

    def get(self, task_id: str) -> Task | None:
        row = self._connection.execute(
            """
            SELECT task_id, instruction, status, result, checkpoint
            FROM tasks
            WHERE task_id = ?
            """,
            (task_id,),
        ).fetchone()

        if row is None:
            return None

        return Task(
            task_id=row[0],
            instruction=row[1],
            status=TaskStatus(row[2]),
            result=row[3],
            checkpoint=row[4],
        )

    def get_running_tasks(self) -> list[Task]:
         rows = self._connection.execute(
            """
                SELECT task_id, instruction, status, result, checkpoint
                FROM tasks
                WHERE status = ?
            """,
            (TaskStatus.RUNNING.value,), ).fetchall()

         return [
             Task(
                 task_id=row[0],
                 instruction=row[1],
                 status=TaskStatus(row[2]),
                 result=row[3],
                 checkpoint=row[4],
             ) for row in rows]