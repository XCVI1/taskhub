from fastapi import APIRouter
import httpx

router = APIRouter()
TASKS_URL = "http://tasks-service:8002/tasks"

@router.get("/")
async def list_tasks():
    async with httpx.AsyncClient() as client:
        r = await client.get(TASKS_URL)
        return r.json()

@router.post("/")
async def create_task(data: dict):
    async with httpx.AsyncClient() as client:
        r = await client.post(TASKS_URL, json=data)
        return r.json()
