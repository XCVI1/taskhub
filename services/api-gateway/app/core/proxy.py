import httpx
from fastapi import HTTPException, Request
from fastapi.responses import Response

async def proxy_request(
    request: Request,
    url: str,
    timeout: float = 10.0,
) -> Response:
    try:
        async with httpx.AsyncClient(timeout=timeout) as client:
            body = await request.body()
            headers = {
                k: v for k, v in request.headers.items()
                if k.lower() not in ("host", "content-length")
            }
            r = await client.request(
                method=request.method,
                url=url,
                headers=headers,
                content=body,
                params=request.query_params,
            )
            return Response(
                content=r.content,
                status_code=r.status_code,
                headers=dict(r.headers),
                media_type=r.headers.get("content-type"),
            )
    except httpx.ConnectError:
        raise HTTPException(status_code=503, detail=f"Service unavailable: {url}")
    except httpx.TimeoutException:
        raise HTTPException(status_code=504, detail=f"Service timeout: {url}")
