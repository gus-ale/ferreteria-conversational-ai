from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.db.session import get_db

router = APIRouter(prefix="/health", tags=["Health"])


@router.get("/live")
async def live() -> dict:
    return {"status": "alive"}


@router.get("/ready")
async def ready(session: AsyncSession = Depends(get_db)) -> dict:
    await session.execute(text("SELECT 1"))
    return {
        "status": "ready",
        "ai_provider": settings.ai_provider,
        "realtime_enabled": settings.realtime_enabled,
    }
