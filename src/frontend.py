import os

from fastapi import FastAPI
from nicegui import app, ui

from src.config import settings


def init_frontend(fastapi_app: FastAPI) -> None:
    @ui.page("/")
    def index_page() -> None:
        port = os.environ.get("PORT", 8000)
        host = app.storage.user.get("host", f"127.0.0.1:{port}")
        ui.label(f"Hello World from {host}")

    ui.run_with(
        fastapi_app,
        mount_path="/_ui",
        storage_secret=settings.STORAGE_SECRET,
    )
