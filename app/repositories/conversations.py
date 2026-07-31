from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.conversation import Conversation, Feedback, Handoff, Message


async def get_or_create_conversation(
    session: AsyncSession,
    conversation_id: str | None,
    *,
    channel: str,
) -> Conversation:
    if conversation_id:
        conversation = await session.get(Conversation, conversation_id)
        if conversation is not None:
            return conversation

    conversation = Conversation(channel=channel)
    session.add(conversation)
    await session.flush()
    return conversation


async def get_conversation(
    session: AsyncSession,
    conversation_id: str,
) -> Conversation | None:
    return await session.get(Conversation, conversation_id)


async def add_message(
    session: AsyncSession,
    conversation_id: str,
    role: str,
    content: str,
    *,
    intent: str | None = None,
    tool_name: str | None = None,
) -> Message:
    message = Message(
        conversation_id=conversation_id,
        role=role,
        content=content,
        intent=intent,
        tool_name=tool_name,
    )
    session.add(message)
    await session.flush()
    return message


async def recent_messages(
    session: AsyncSession,
    conversation_id: str,
    *,
    limit: int,
) -> list[Message]:
    statement = (
        select(Message)
        .where(Message.conversation_id == conversation_id)
        .order_by(Message.created_at.desc(), Message.id.desc())
        .limit(limit)
    )
    result = await session.scalars(statement)
    return list(reversed(result.all()))


async def all_messages(
    session: AsyncSession,
    conversation_id: str,
) -> list[Message]:
    statement = (
        select(Message)
        .where(Message.conversation_id == conversation_id)
        .order_by(Message.created_at.asc(), Message.id.asc())
    )
    result = await session.scalars(statement)
    return list(result.all())


async def create_handoff(
    session: AsyncSession,
    conversation: Conversation,
    reason: str,
) -> Handoff:
    handoff = Handoff(conversation_id=conversation.id, reason=reason)
    conversation.status = "waiting_human"
    session.add(handoff)
    await session.flush()
    return handoff


async def create_feedback(
    session: AsyncSession,
    conversation_id: str,
    rating: int,
    comment: str | None,
) -> Feedback:
    feedback = Feedback(
        conversation_id=conversation_id,
        rating=rating,
        comment=comment,
    )
    session.add(feedback)
    await session.flush()
    return feedback
