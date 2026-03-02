from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.core.security import hash_password, verify_password, create_access_token


async def register_user(
    db: AsyncSession, username: str, password: str, email: str
) -> User | None:
    # Check if email already exists
    result = await db.execute(select(User).where(User.Email == email))
    if result.scalars().first():
        return None

    # Check if username already exists
    result = await db.execute(select(User).where(User.Username == username))
    if result.scalars().first():
        return None

    user = User(
        Username=username,
        Email=email,
        PasswordHash=hash_password(password),
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


async def login_user(db: AsyncSession, email: str, password: str) -> str | None:
    result = await db.execute(select(User).where(User.Email == email))
    user = result.scalars().first()
    if not user:
        return None

    if not verify_password(password, user.PasswordHash):
        return None

    return create_access_token(user.Id, user.Username)
