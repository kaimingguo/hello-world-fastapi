from fastapi import FastAPI
from nicegui import ui


def init_frontend(fastapi_app: FastAPI) -> None:
    @ui.page("/")
    def index_page() -> None:
        ui.label("Hello World!")

    ui.run_with(
        fastapi_app,
        mount_path="/_ui",
    )
