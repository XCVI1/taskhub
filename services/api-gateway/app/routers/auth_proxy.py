from fastapi import APIRouter
import httpx

router = APIRouter()
AUTH_URL = "http://auth-service:8001/auth"

@router.post("/login")
async def login(data: dict):
    async with httpx.AsyncClient() as client:
        r = await client.post(f"{AUTH_URL}/login", json=data)
        return r.json()

@router.post("/register")
async def register(data: dict):
    async with httpx.AsyncClient() as client:
        r = await client.post(f"{AUTH_URL}/register", json=data)
        return r.json()
