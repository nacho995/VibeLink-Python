from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user_likes import UserLikes


async def calculate_compatibility(
    db: AsyncSession, user_id_1: int, user_id_2: int
) -> int:
    result1 = await db.execute(
        select(UserLikes).where(UserLikes.UserId == user_id_1)
    )
    likes1 = result1.scalars().all()

    result2 = await db.execute(
        select(UserLikes).where(UserLikes.UserId == user_id_2)
    )
    likes2 = result2.scalars().all()

    ids1 = {ul.ContentId for ul in likes1}
    ids2 = {ul.ContentId for ul in likes2}

    common = ids1 & ids2
    menor = min(len(ids1), len(ids2))

    if menor == 0:
        return 0

    percentage = (len(common) / menor) * 100
    return int(percentage)
