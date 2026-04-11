from fastapi import FastAPI
from app.events.handler import get_notifications

app = FastAPI(title="Notifications Service")

@app.get("/notifications")
async def notifications():
    return get_notifications()
