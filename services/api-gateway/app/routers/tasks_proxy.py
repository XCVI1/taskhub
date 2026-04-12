from fastapi import APIRouter, Request
from fastapi.responses import Response
from app.core.proxy import proxy_request
from app.core.config import settings

router = APIRouter()

@router.api_route("/{path:path}", methods=["GET", "POST", "PUT", "PATCH", "DELETE"])
async def tasks_proxy(path: str, request: Request) -> Response:
    url = f"{settings.TASKS_SERVICE_URL}/tasks/{path}"
    return await proxy_request(request, url)
