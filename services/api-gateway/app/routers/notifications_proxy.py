from fastapi import APIRouter
import httpx

router = APIRouter()
NOTIF_URL = "http://notifications-service:8003/notifications"

@router.get("/")
async def get_notifications():
    async with httpx.AsyncClient() as client:
        r = await client.get(NOTIF_URL)
        return r.json()
