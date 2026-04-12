from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import httpx
from app.core.config import settings

bearer = HTTPBearer()

async def get_current_user_id(
    credentials: HTTPAuthorizationCredentials = Depends(bearer),
) -> str:
    token = credentials.credentials
    try:
        async with httpx.AsyncClient() as client:
            r = await client.post(
                f"{settings.AUTH_SERVICE_URL}/auth/validate",
                params={"token": token},
            )
            data = r.json()
            if not data.get("valid"):
                raise HTTPException(status_code=401, detail="Invalid token")
            return data["user_id"]
    except httpx.ConnectError:
        raise HTTPException(status_code=503, detail="auth-service unavailable")
