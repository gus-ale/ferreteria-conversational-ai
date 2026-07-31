from fastapi import Depends, Request
from openai import AsyncOpenAI
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.db.session import get_db
from app.services.agent import AgentService
from app.services.realtime import RealtimeService
from app.services.tools import ToolExecutor


def get_openai_client(request: Request) -> AsyncOpenAI | None:
    return request.app.state.openai_client


async def get_agent_service(
    session: AsyncSession = Depends(get_db),
    openai_client: AsyncOpenAI | None = Depends(get_openai_client),
) -> AgentService:
    return AgentService(
        session=session,
        tool_executor=ToolExecutor(session),
        settings=settings,
        openai_client=openai_client,
    )


def get_realtime_service() -> RealtimeService:
    return RealtimeService(settings)
