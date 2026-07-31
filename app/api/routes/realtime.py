from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import get_realtime_service
from app.core.config import settings
from app.db.session import get_db
from app.repositories import conversations as conversation_repository
from app.schemas.chat import (
    RealtimeTokenRequest,
    RealtimeToolRequest,
    RealtimeToolResponse,
)
from app.services.realtime import RealtimeService
from app.services.tools import ToolExecutor

router = APIRouter(prefix="/realtime", tags=["Realtime voice"])


@router.get("/config")
async def realtime_config() -> dict:
    return {
        "enabled": settings.realtime_enabled,
        "model": settings.openai_realtime_model if settings.realtime_enabled else None,
        "voice": settings.openai_realtime_voice if settings.realtime_enabled else None,
    }


@router.post("/token")
async def realtime_token(
    data: RealtimeTokenRequest,
    service: RealtimeService = Depends(get_realtime_service),
) -> dict:
    return await service.create_client_secret(data.user_id)


@router.post("/tool", response_model=RealtimeToolResponse)
async def execute_realtime_tool(
    data: RealtimeToolRequest,
    session: AsyncSession = Depends(get_db),
) -> RealtimeToolResponse:
    conversation = await conversation_repository.get_or_create_conversation(
        session,
        data.conversation_id,
        channel="voice",
    )
    executor = ToolExecutor(session)
    result = await executor.execute(
        data.name,
        data.arguments,
        conversation_id=conversation.id,
    )
    await conversation_repository.add_message(
        session,
        conversation.id,
        "tool",
        executor.serialize(result),
        tool_name=data.name,
    )
    await session.commit()
    return RealtimeToolResponse(
        conversation_id=conversation.id,
        output=result.output,
    )
