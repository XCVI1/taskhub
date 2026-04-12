from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from app.core.database import get_db, get_engine, Base
from app.routers.tasks import router as tasks_router
import app.models.task  # noqa: F401 — чтобы Base увидел модели

app = FastAPI(title="Tasks Service")

@app.on_event("startup")
async def startup():
    async with get_engine().begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

app.include_router(tasks_router, prefix="/tasks")

@app.get("/health/live")
async def liveness():
    return {"status": "ok", "service": "tasks"}

@app.get("/health/ready")
async def readiness(db: AsyncSession = Depends(get_db)):
    try:
        await db.execute(text("SELECT 1"))
        return {"status": "ok", "db": "ok"}
    except Exception:
        raise HTTPException(status_code=503, detail="db unavailable")
