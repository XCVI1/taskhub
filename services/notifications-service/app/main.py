from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from app.core.database import get_db, get_engine, Base
from app.routers.notifications import router as notifications_router
from app.routers.notifications import internal_router
import app.models.notification  # noqa: F401

app = FastAPI(title="Notifications Service")

@app.on_event("startup")
async def startup():
    async with get_engine().begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

app.include_router(notifications_router, prefix="/notifications")
app.include_router(internal_router, prefix="/notifications")

@app.get("/health/live")
async def liveness():
    return {"status": "ok", "service": "notifications"}

@app.get("/health/ready")
async def readiness(db: AsyncSession = Depends(get_db)):
    try:
        await db.execute(text("SELECT 1"))
        return {"status": "ok", "db": "ok"}
    except Exception:
        raise HTTPException(status_code=503, detail="db unavailable")
