from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.security import get_current_user_id
from app.models.user import User
from app.models.swipe import Swipe, SwipeState
from app.models.match import Match
from app.schemas.swipe import PeopleSwipeDTO

router = APIRouter(prefix="/api/Swipe", tags=["Swipe"])


@router.post("")
async def swipe(
    dto: PeopleSwipeDTO,
    db: AsyncSession = Depends(get_db),
    _current_user: int = Depends(get_current_user_id),
):
    user = await db.get(User, dto.user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    # Swipe limit for non-premium
    if not user.IsPremium:
        if user.LastSwipeUpdate.date() != datetime.now(timezone.utc).date():
            user.Swipes = 10
            user.LastSwipeUpdate = datetime.now(timezone.utc)
        if user.Swipes <= 0:
            raise HTTPException(
                status_code=400,
                detail="No te quedan Swipes. Hazte premium!",
            )
        user.Swipes -= 1

    swipe_state = SwipeState(dto.state)
    new_swipe = Swipe(
        UserId=dto.user_id,
        MatchingUserId=dto.matching_user_id,
        State=swipe_state,
    )
    db.add(new_swipe)

    if swipe_state == SwipeState.Like:
        # Check mutual match
        result = await db.execute(
            select(Swipe).where(
                and_(
                    Swipe.UserId == dto.matching_user_id,
                    Swipe.MatchingUserId == dto.user_id,
                    Swipe.State == SwipeState.Like,
                )
            )
        )
        mutual = result.scalars().first()

        if mutual:
            # Check if match already exists
            result = await db.execute(
                select(Match).where(
                    (
                        (Match.UserId == dto.user_id)
                        & (Match.MatchingUserId == dto.matching_user_id)
                    )
                    | (
                        (Match.UserId == dto.matching_user_id)
                        & (Match.MatchingUserId == dto.user_id)
                    )
                )
            )
            existing_match = result.scalars().first()

            if not existing_match:
                new_match = Match(
                    UserId=dto.user_id,
                    MatchingUserId=dto.matching_user_id,
                    Date=datetime.now(timezone.utc),
                )
                db.add(new_match)
                await db.commit()
                await db.refresh(new_match)
                return {
                    "id": new_match.Id,
                    "userId": new_match.UserId,
                    "matchingUserId": new_match.MatchingUserId,
                    "date": new_match.Date.isoformat(),
                }

    await db.commit()
    return {"message": "OK"}


@router.get("")
async def get_swipes(
    db: AsyncSession = Depends(get_db),
    _current_user: int = Depends(get_current_user_id),
):
    result = await db.execute(select(Swipe))
    swipes = result.scalars().all()
    return [
        {
            "id": s.Id,
            "userId": s.UserId,
            "matchingUserId": s.MatchingUserId,
            "state": s.State.value,
        }
        for s in swipes
    ]


@router.get("/{swipe_id}")
async def get_swipe(
    swipe_id: int,
    db: AsyncSession = Depends(get_db),
    _current_user: int = Depends(get_current_user_id),
):
    swipe = await db.get(Swipe, swipe_id)
    if not swipe:
        raise HTTPException(status_code=404, detail="Not found")
    return {
        "id": swipe.Id,
        "userId": swipe.UserId,
        "matchingUserId": swipe.MatchingUserId,
        "state": swipe.State.value,
    }
