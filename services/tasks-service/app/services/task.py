import httpx
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.task import TaskRepository
from app.core.config import settings

class TaskService:
    def __init__(self, db: AsyncSession):
        self.repo = TaskRepository(db)

    async def get_all(self, user_id: str):
        return await self.repo.get_all(user_id)

    async def get_by_id(self, task_id: str, user_id: str):
        task = await self.repo.get_by_id(task_id, user_id)
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        return task

    async def create(self, user_id: str, title: str, description: str | None):
        task = await self.repo.create(user_id=user_id, title=title, description=description)
        await self._notify(
            user_id=user_id,
            message=f"Task '{task.title}' created",
            task_id=task.id,
            event="task_created",
        )
        return task

    async def update(self, task_id: str, user_id: str, **kwargs):
        task = await self.get_by_id(task_id, user_id)
        updated = await self.repo.update(task, **kwargs)
        await self._notify(
            user_id=user_id,
            message=f"Task '{updated.title}' updated",
            task_id=updated.id,
            event="task_updated",
        )
        return updated

    async def delete(self, task_id: str, user_id: str):
        task = await self.get_by_id(task_id, user_id)
        await self._notify(
            user_id=user_id,
            message=f"Task '{task.title}' deleted",
            task_id=task.id,
            event="task_deleted",
        )
        await self.repo.delete(task)

    async def _notify(self, user_id: str, message: str, task_id: str, event: str):
        try:
            async with httpx.AsyncClient() as client:
                await client.post(
                    f"{settings.NOTIFICATIONS_SERVICE_URL}/notifications/internal",
                    json={
                        "user_id": user_id,
                        "message": message,
                        "task_id": task_id,
                        "event": event,
                    },
                    timeout=3.0,
                )
        except Exception:
            pass
