from fastapi import FastAPI
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
