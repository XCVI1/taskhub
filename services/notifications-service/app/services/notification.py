from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.notification import NotificationRepository

class NotificationService:
    def __init__(self, db: AsyncSession):
        self.repo = NotificationRepository(db)

    async def get_all(self, user_id: str):
        return await self.repo.get_all(user_id)

    async def get_unread(self, user_id: str):
        return await self.repo.get_unread(user_id)

    async def create(self, user_id: str, task_id: str, event: str, message: str):
        return await self.repo.create(
            user_id=user_id,
            task_id=task_id,
            event=event,
            message=message,
        )

    async def mark_read(self, notification_id: str, user_id: str):
        notification = await self.repo.mark_read(notification_id, user_id)
        if not notification:
            raise HTTPException(status_code=404, detail="Notification not found")
        return notification

    async def mark_all_read(self, user_id: str):
        await self.repo.mark_all_read(user_id)
        return {"status": "ok"}
