from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import httpx
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.services.notification import NotificationService
from app.schemas.notification import NotificationCreate, NotificationResponse

router = APIRouter()
internal_router = APIRouter()
bearer = HTTPBearer()

async def get_current_user_id(
    credentials: HTTPAuthorizationCredentials = Depends(bearer),
) -> str:
    token = credentials.credentials
    try:
        async with httpx.AsyncClient() as client:
            r = await client.post(
                "http://auth-service:8001/auth/validate",
                params={"token": token},
            )
            data = r.json()
            if not data.get("valid"):
                from fastapi import HTTPException
                raise HTTPException(status_code=401, detail="Invalid token")
            return data["user_id"]
    except httpx.ConnectError:
        from fastapi import HTTPException
        raise HTTPException(status_code=503, detail="auth-service unavailable")

@router.get("/", response_model=list[NotificationResponse])
async def list_notifications(
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    return await NotificationService(db).get_all(user_id)

@router.get("/unread", response_model=list[NotificationResponse])
async def unread_notifications(
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    return await NotificationService(db).get_unread(user_id)

@router.patch("/{notification_id}/read", response_model=NotificationResponse)
async def mark_read(
    notification_id: str,
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    return await NotificationService(db).mark_read(notification_id, user_id)

@router.patch("/read-all", response_model=dict)
async def mark_all_read(
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    return await NotificationService(db).mark_all_read(user_id)

@internal_router.post("/internal")
async def receive_notification(
    data: NotificationCreate,
    db: AsyncSession = Depends(get_db),
):
    return await NotificationService(db).create(
        user_id=data.user_id,
        task_id=data.task_id,
        event=data.event,
        message=data.message,
    )
