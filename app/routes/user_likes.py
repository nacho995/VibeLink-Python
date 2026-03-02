from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.security import get_current_user_id
from app.models.user import User
from app.models.user_likes import UserLikes, LikeState
from app.models.content import Content, ContentType
from app.schemas.swipe import SwipeDTO, ExternalLikeDTO

router = APIRouter(prefix="/api/UserLikes", tags=["UserLikes"])


async def _check_swipes(user: User) -> None:
    """Check and update swipe count for non-premium users."""
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


@router.post("")
async def create_user_like(
    dto: SwipeDTO,
    db: AsyncSession = Depends(get_db),
    _current_user: int = Depends(get_current_user_id),
):
    user = await db.get(User, dto.user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    await _check_swipes(user)

    state = LikeState(dto.state)
    user_like = UserLikes(
        UserId=dto.user_id,
        ContentId=dto.content_id,
        State=state,
        Punctuation=10 if state == LikeState.Liked else 0,
    )
    db.add(user_like)
    await db.commit()
    return {"message": "OK"}


@router.get("")
async def get_swipes(
    db: AsyncSession = Depends(get_db),
    _current_user: int = Depends(get_current_user_id),
):
    result = await db.execute(select(UserLikes))
    swipes = result.scalars().all()
    return [
        {
            "contentId": s.ContentId,
            "state": s.State.value,
            "userId": s.UserId,
            "punctuation": s.Punctuation,
        }
        for s in swipes
    ]


@router.get("/{like_id}")
async def get_user_like(
    like_id: int,
    db: AsyncSession = Depends(get_db),
    _current_user: int = Depends(get_current_user_id),
):
    user_like = await db.get(UserLikes, like_id)
    if not user_like:
        raise HTTPException(status_code=404, detail="Not found")
    return {
        "contentId": user_like.ContentId,
        "state": user_like.State.value,
        "punctuation": user_like.Punctuation,
    }


@router.post("/external")
async def external_like(
    dto: ExternalLikeDTO,
    db: AsyncSession = Depends(get_db),
    _current_user: int = Depends(get_current_user_id),
):
    user = await db.get(User, dto.user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    # Parse ExternalId
    parts = dto.external_id.split("-")
    if len(parts) < 2:
        raise HTTPException(
            status_code=400,
            detail="ExternalId invalido. Formato: tmdb-movie-123, tmdb-tv-123, o igdb-123",
        )

    source = parts[0]  # "tmdb" or "igdb"

    if source == "igdb":
        type_str = "game"
        api_id_str = "-".join(parts[1:])
    else:
        if len(parts) < 3:
            raise HTTPException(
                status_code=400,
                detail="ExternalId TMDB invalido. Formato: tmdb-movie-123 o tmdb-tv-123",
            )
        type_str = parts[1]
        api_id_str = "-".join(parts[2:])

    try:
        api_id = int(api_id_str)
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail="ExternalId invalido: el ID debe ser numerico",
        )

    # Map type string to ContentType enum
    content_type_map = {
        "movie": ContentType.pelicula,
        "tv": ContentType.serie,
    }
    content_type = content_type_map.get(type_str, ContentType.videojuego)

    # Find or create content
    result = await db.execute(
        select(Content).where(Content.ApiId == api_id, Content.Type == content_type)
    )
    content = result.scalars().first()

    if not content:
        content = Content(
            ApiId=api_id,
            Type=content_type,
            Titulo=dto.title,
            ImagenUrl=dto.image_url,
            Año=datetime.now(timezone.utc).year,
        )
        db.add(content)
        await db.commit()
        await db.refresh(content)

    # Check swipes
    await _check_swipes(user)

    # Check for duplicate like
    existing = await db.execute(
        select(UserLikes).where(
            UserLikes.UserId == dto.user_id,
            UserLikes.ContentId == content.Id,
        )
    )
    if existing.scalars().first():
        return {"message": "Ya tienes este contenido en tus likes", "contentId": content.Id}

    state = LikeState(dto.state)
    user_like = UserLikes(
        UserId=dto.user_id,
        ContentId=content.Id,
        State=state,
        Punctuation=10 if state == LikeState.Liked else 0,
    )
    db.add(user_like)
    await db.commit()
    return {"message": "Like guardado", "contentId": content.Id}
