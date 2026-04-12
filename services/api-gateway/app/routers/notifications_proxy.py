from fastapi import APIRouter, Request
from fastapi.responses import Response
from app.core.proxy import proxy_request
from app.core.config import settings

router = APIRouter()

@router.api_route("/{path:path}", methods=["GET", "POST", "PUT", "PATCH", "DELETE"])
async def notifications_proxy(path: str, request: Request) -> Response:
    url = f"{settings.NOTIFICATIONS_SERVICE_URL}/notifications/{path}"
    return await proxy_request(request, url)
