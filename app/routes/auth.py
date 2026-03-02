from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.schemas.auth import RegisterDTO, LoginDTO
from app.schemas.user import UserResponse
from app.services.auth_service import register_user, login_user

router = APIRouter(prefix="/api/Auth", tags=["Auth"])


@router.post("/register")
async def register(dto: RegisterDTO, db: AsyncSession = Depends(get_db)):
    if dto.password != dto.confirm_password:
        raise HTTPException(status_code=400, detail="Las contrasenas no coinciden")

    user = await register_user(db, dto.username, dto.password, dto.email)
    if user is None:
        raise HTTPException(status_code=400, detail="El usuario ya existe")

    return {
        "id": user.Id,
        "username": user.Username,
        "email": user.Email,
        "isPremium": user.IsPremium,
        "swipes": user.Swipes,
    }


@router.post("/login")
async def login(dto: LoginDTO, db: AsyncSession = Depends(get_db)):
    token = await login_user(db, dto.email, dto.password)
    if token is None:
        raise HTTPException(status_code=400, detail="Credenciales incorrectas")

    return token
