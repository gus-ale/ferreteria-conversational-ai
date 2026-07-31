from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.errors import NotFoundError
from app.db.session import get_db
from app.repositories import conversations as conversation_repository
from app.schemas.chat import (
    FeedbackCreate,
    FeedbackRead,
    HandoffCreate,
    HandoffRead,
)

router = APIRouter(tags=["Conversation workflows"])


@router.post(
    "/handoffs",
    response_model=HandoffRead,
    status_code=status.HTTP_201_CREATED,
)
async def create_handoff(
    data: HandoffCreate,
    session: AsyncSession = Depends(get_db),
) -> HandoffRead:
    conversation = await conversation_repository.get_conversation(
        session,
        data.conversation_id,
    )
    if conversation is None:
        raise NotFoundError("Conversación no encontrada")
    handoff = await conversation_repository.create_handoff(
        session,
        conversation,
        data.reason,
    )
    await session.commit()
    return HandoffRead(
        id=handoff.id,
        conversation_id=handoff.conversation_id,
        reason=handoff.reason,
        status=handoff.status,
    )


@router.post(
    "/feedback",
    response_model=FeedbackRead,
    status_code=status.HTTP_201_CREATED,
)
async def create_feedback(
    data: FeedbackCreate,
    session: AsyncSession = Depends(get_db),
) -> FeedbackRead:
    conversation = await conversation_repository.get_conversation(
        session,
        data.conversation_id,
    )
    if conversation is None:
        raise NotFoundError("Conversación no encontrada")
    feedback = await conversation_repository.create_feedback(
        session,
        conversation.id,
        data.rating,
        data.comment,
    )
    await session.commit()
    return FeedbackRead(
        id=feedback.id,
        conversation_id=feedback.conversation_id,
        rating=feedback.rating,
        comment=feedback.comment,
    )
