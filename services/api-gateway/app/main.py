from fastapi import FastAPI, HTTPException
from app.routers.auth_proxy import router as auth_router
from app.routers.tasks_proxy import router as tasks_router
from app.routers.notifications_proxy import router as notif_router

app = FastAPI(title="API Gateway")

app.include_router(auth_router, prefix="/auth")
app.include_router(tasks_router, prefix="/tasks")
app.include_router(notif_router, prefix="/notifications")

@app.get("/")
async def root():
    return {"message": "API Gateway is running"}

@app.get("/health/live")
async def liveness():
    return {"status": "ok", "service": "api-gateway"}

@app.get("/health/ready")
async def readiness():
    import httpx
    from app.core.config import settings

    services = {
        "auth": f"{settings.AUTH_SERVICE_URL}/health/live",
        "tasks": f"{settings.TASKS_SERVICE_URL}/health/live",
        "notifications": f"{settings.NOTIFICATIONS_SERVICE_URL}/health/live",
    }
    results = {}
    async with httpx.AsyncClient(timeout=3.0) as client:
        for name, url in services.items():
            try:
                r = await client.get(url)
                results[name] = "ok" if r.status_code == 200 else "degraded"
            except Exception:
                results[name] = "unavailable"

    degraded = [k for k, v in results.items() if v != "ok"]
    if degraded:
        raise HTTPException(status_code=503, detail={"services": results})

    return {"status": "ok", "services": results}
