import os

from fastapi import FastAPI
from nicegui import app, ui

from src.config import settings


def init_frontend(fastapi_app: FastAPI) -> None:
    @ui.page("/")
    def index_page() -> None:
        host = app.storage.user["host"]
        ui.label(f"Hello World from {host}")

    ui.run_with(
        fastapi_app,
        mount_path="/_ui",
        storage_secret=settings.STORAGE_SECRET,
    )
