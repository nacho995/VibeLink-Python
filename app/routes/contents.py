from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.security import get_current_user_id
from app.models.content import Content

router = APIRouter(prefix="/api/ContentsControllers", tags=["Contents"])


@router.get("")
async def get_contents(
    db: AsyncSession = Depends(get_db),
    _current_user: int = Depends(get_current_user_id),
):
    result = await db.execute(select(Content))
    contents = result.scalars().all()
    return [
        {
            "id": c.Id,
            "type": c.Type.value,
            "apiId": c.ApiId,
            "titulo": c.Titulo,
            "imagenUrl": c.ImagenUrl,
            "generos": c.Generos,
            "año": c.Año,
        }
        for c in contents
    ]


@router.get("/{content_id}")
async def get_content_by_id(
    content_id: int,
    db: AsyncSession = Depends(get_db),
    _current_user: int = Depends(get_current_user_id),
):
    content = await db.get(Content, content_id)
    if not content:
        raise HTTPException(status_code=404, detail="Not found")
    return {
        "id": content.Id,
        "type": content.Type.value,
        "apiId": content.ApiId,
        "titulo": content.Titulo,
        "imagenUrl": content.ImagenUrl,
        "generos": content.Generos,
        "año": content.Año,
    }


@router.post("")
async def create_content(
    content_data: dict,
    db: AsyncSession = Depends(get_db),
    _current_user: int = Depends(get_current_user_id),
):
    from app.models.content import ContentType

    content = Content(
        Type=ContentType(content_data.get("type", "pelicula")),
        ApiId=content_data.get("apiId", 0),
        Titulo=content_data.get("titulo", ""),
        ImagenUrl=content_data.get("imagenUrl"),
        Generos=content_data.get("generos"),
        Año=content_data.get("año", 0),
    )
    db.add(content)
    await db.commit()
    await db.refresh(content)
    return {
        "id": content.Id,
        "type": content.Type.value,
        "apiId": content.ApiId,
        "titulo": content.Titulo,
        "imagenUrl": content.ImagenUrl,
        "generos": content.Generos,
        "año": content.Año,
    }
