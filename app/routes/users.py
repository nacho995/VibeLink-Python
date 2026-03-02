from datetime import timezone

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.security import get_current_user_id
from app.models.user import User, Gender
from app.schemas.user import ProfileUpdateDTO

router = APIRouter(prefix="/api/Users", tags=["Users"])


def _user_to_response(user: User) -> dict:
    return {
        "id": user.Id,
        "username": user.Username,
        "email": user.Email,
        "avatarUrl": user.AvatarUrl,
        "codigoInvitacion": user.CodigoInvitacion,
        "fechaRegistro": user.FechaRegistro.isoformat() if user.FechaRegistro else None,
        "gender": user.Gender.value if user.Gender else None,
        "dateOfBirth": user.DateOfBirth.isoformat() if user.DateOfBirth else None,
        "bio": user.Bio,
        "isPremium": user.IsPremium,
        "swipes": user.Swipes,
    }


@router.get("")
async def get_users(
    db: AsyncSession = Depends(get_db),
    _current_user: int = Depends(get_current_user_id),
):
    result = await db.execute(select(User))
    users = result.scalars().all()
    return [_user_to_response(u) for u in users]


@router.get("/{user_id}")
async def get_user(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    _current_user: int = Depends(get_current_user_id),
):
    user = await db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return _user_to_response(user)


@router.put("/{user_id}")
async def update_user(
    user_id: int,
    dto: ProfileUpdateDTO,
    db: AsyncSession = Depends(get_db),
    _current_user: int = Depends(get_current_user_id),
):
    user = await db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if dto.avatar_url is not None:
        user.AvatarUrl = dto.avatar_url
    user.Gender = Gender(dto.gender)
    user.DateOfBirth = dto.date_of_birth.replace(tzinfo=timezone.utc)
    if dto.bio is not None:
        user.Bio = dto.bio

    await db.commit()
    await db.refresh(user)
    return _user_to_response(user)
