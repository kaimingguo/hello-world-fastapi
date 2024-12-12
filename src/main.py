import logging
import time
import ipaddress
from typing import Dict

from fastapi import FastAPI, Request

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
async def ip_logging(request: Request, call_next):
    client_ip = request.client.host
    client_ip_obj = ipaddress.ip_address(client_ip)
    logger.info(f"Client IP: {client_ip_obj}")

    response = await call_next(request)
    return response


@app.get("/")
async def health() -> Dict[str, str]:
    return {"status": "healthy"}
