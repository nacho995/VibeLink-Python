from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, and_, or_
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.security import get_current_user_id
from app.models.match import Match
from app.models.message_chat import MessageChat
from app.schemas.message import MessageDTO

router = APIRouter(prefix="/api/Chat", tags=["Chat"])


@router.post("")
async def send_message(
    dto: MessageDTO,
    db: AsyncSession = Depends(get_db),
    _current_user: int = Depends(get_current_user_id),
):
    # Check that they have a match
    result = await db.execute(
        select(Match).where(
            or_(
                and_(
                    Match.UserId == dto.user_id,
                    Match.MatchingUserId == dto.matching_user_id,
                ),
                and_(
                    Match.UserId == dto.matching_user_id,
                    Match.MatchingUserId == dto.user_id,
                ),
            )
        )
    )
    match = result.scalars().first()
    if not match:
        raise HTTPException(
            status_code=400, detail="No tienen match, no pueden chatear"
        )

    message = MessageChat(
        UserId=dto.user_id,
        MatchingUserId=dto.matching_user_id,
        Message=dto.message,
        Date=datetime.now(timezone.utc),
    )
    db.add(message)
    await db.commit()
    await db.refresh(message)

    return {
        "id": message.Id,
        "userId": message.UserId,
        "matchingUserId": message.MatchingUserId,
        "message": message.Message,
        "date": message.Date.isoformat(),
    }


@router.get("")
async def get_messages(
    userId: int,
    matchingUserId: int,
    db: AsyncSession = Depends(get_db),
    _current_user: int = Depends(get_current_user_id),
):
    result = await db.execute(
        select(MessageChat)
        .where(
            or_(
                and_(
                    MessageChat.UserId == userId,
                    MessageChat.MatchingUserId == matchingUserId,
                ),
                and_(
                    MessageChat.UserId == matchingUserId,
                    MessageChat.MatchingUserId == userId,
                ),
            )
        )
        .order_by(MessageChat.Date)
    )
    messages = result.scalars().all()

    return [
        {
            "id": m.Id,
            "userId": m.UserId,
            "matchingUserId": m.MatchingUserId,
            "message": m.Message,
            "date": m.Date.isoformat(),
        }
        for m in messages
    ]
