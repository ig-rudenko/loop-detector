from fastapi import FastAPI
from loguru import logger
from uvicorn import server

from app.handlers.auth import router as auth_router
from app.handlers.graph import router as graph_router
from app.handlers.log_messages import router as log_messages_router
from app.middlewares.logging import LoggingMiddleware
from app.services.logging import setup_logger
from app.settings import settings

setup_logger(settings.log_level)
server.logger = logger
app = FastAPI()
app.add_middleware(LoggingMiddleware, logger=logger)

app.include_router(auth_router, prefix="/api/v1")
app.include_router(graph_router, prefix="/api/v1")
app.include_router(log_messages_router, prefix="/api/v1")


@app.get("/ping", tags=["health"])
async def status():
    return {"message": "pong"}
