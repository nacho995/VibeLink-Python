from fastapi import APIRouter, Depends
from sqlalchemy import select, or_
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.security import get_current_user_id
from app.models.user import User
from app.models.match import Match
from app.services.compatibility_service import calculate_compatibility

router = APIRouter(prefix="/api/Matching", tags=["Matching"])


@router.get("/{user_id}")
async def get_matches(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    _current_user: int = Depends(get_current_user_id),
):
    # Get all users except the current one
    result = await db.execute(select(User).where(User.Id != user_id))
    users = result.scalars().all()

    # Calculate compatibility for each user
    results = []
    for usuario in users:
        compatibility = await calculate_compatibility(db, user_id, usuario.Id)
        results.append(
            {
                "usuario": {
                    "id": usuario.Id,
                    "username": usuario.Username,
                    "avatarUrl": usuario.AvatarUrl,
                    "bio": usuario.Bio,
                    "gender": usuario.Gender.value if usuario.Gender else None,
                    "dateOfBirth": usuario.DateOfBirth.isoformat() if usuario.DateOfBirth else None,
                },
                "compatibilidad": compatibility,
            }
        )

    # Sort by compatibility descending
    results.sort(key=lambda r: r["compatibilidad"], reverse=True)
    return results


@router.get("/mymatch/{user_id}")
async def see_matches(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    _current_user: int = Depends(get_current_user_id),
):
    result = await db.execute(
        select(Match).where(
            or_(Match.UserId == user_id, Match.MatchingUserId == user_id)
        )
    )
    matches = result.scalars().all()

    results = []
    for match in matches:
        another_user_id = (
            match.MatchingUserId if match.UserId == user_id else match.UserId
        )
        another_user = await db.get(User, another_user_id)
        if not another_user:
            continue

        results.append(
            {
                "matchId": match.Id,
                "matchDate": match.Date.isoformat() if match.Date else None,
                "anotherUser": {
                    "id": another_user_id,
                    "username": another_user.Username,
                    "avatarUrl": another_user.AvatarUrl,
                    "bio": another_user.Bio,
                },
            }
        )

    return results
