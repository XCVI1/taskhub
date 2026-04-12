from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.task import Task

class TaskRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(self, user_id: str) -> list[Task]:
        result = await self.db.execute(
            select(Task).where(Task.user_id == user_id).order_by(Task.created_at.desc())
        )
        return list(result.scalars().all())

    async def get_by_id(self, task_id: str, user_id: str) -> Task | None:
        result = await self.db.execute(
            select(Task).where(Task.id == task_id, Task.user_id == user_id)
        )
        return result.scalar_one_or_none()

    async def create(self, user_id: str, title: str, description: str | None) -> Task:
        task = Task(user_id=user_id, title=title, description=description)
        self.db.add(task)
        await self.db.commit()
        await self.db.refresh(task)
        return task

    async def update(self, task: Task, **kwargs) -> Task:
        for key, value in kwargs.items():
            if value is not None:
                setattr(task, key, value)
        await self.db.commit()
        await self.db.refresh(task)
        return task

    async def delete(self, task: Task) -> None:
        await self.db.delete(task)
        await self.db.commit()
