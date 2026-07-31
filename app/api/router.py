from fastapi import APIRouter

from app.api.routes import chat, health, realtime, workflows

api_router = APIRouter()
api_router.include_router(health.router)
api_router.include_router(chat.router)
api_router.include_router(workflows.router)
api_router.include_router(realtime.router)
