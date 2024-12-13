import ipaddress
import logging
import time
from typing import Dict

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from nicegui import app

from src.config import settings
from src.frontend import init_frontend

ALLOWED_NETWORKS = [
    ipaddress.ip_network(ip.strip()) for ip in settings.INTERNAL_ALLOWED_LIST
]

logger = logging.getLogger("uvicorn.error")

app = FastAPI(openapi_url="/openapi.json")


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.perf_counter()
    response = await call_next(request)
    process_time = time.perf_counter() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


@app.middleware("http")
async def ip_restriction(request: Request, call_next):
    path = request.url.path
    is_protected = any(
        path.startswith(protected_path)
        for protected_path in settings.PROTECTED_PATHS
    )
    if is_protected:
        client_ip = request.client.host
        client_ip_obj = ipaddress.ip_address(client_ip)

        is_allowed = any(
            client_ip_obj in network for network in ALLOWED_NETWORKS
        )

        if not is_allowed:
            return JSONResponse(
                status_code=status.HTTP_403_FORBIDDEN,
                content={
                    "error": "Access denied",
                    "message": "Your IP is not allowed to access this resource",
                },
            )

    return await call_next(request)


@app.middleware("http")
async def add_host_header(request: Request, call_next):
    if "x-forwarded-host" in request.headers:
        host = request.headers["x-forwarded-host"].encode()
        request.scope["headers"].append((b"host", host))
        app.storage.user["host"] = host
    return await call_next(request)


@app.get("/")
async def health() -> Dict[str, str]:
    return {"status": "healthy"}


init_frontend(app)
