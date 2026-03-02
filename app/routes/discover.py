from fastapi import APIRouter, Depends, HTTPException, Query

from app.core.security import get_current_user_id
from app.services.content_service import (
    get_discovery_content,
    get_popular_movies,
    get_popular_series,
    get_popular_games,
    search_all,
    search_movies_and_series,
    search_games,
)

router = APIRouter(prefix="/api/Discover", tags=["Discover"])


@router.get("")
async def discover(
    page: int = Query(1),
    _current_user: int = Depends(get_current_user_id),
):
    return await get_discovery_content(page)


@router.get("/movies")
async def discover_movies(
    page: int = Query(1),
    _current_user: int = Depends(get_current_user_id),
):
    return await get_popular_movies(page)


@router.get("/series")
async def discover_series(
    page: int = Query(1),
    _current_user: int = Depends(get_current_user_id),
):
    return await get_popular_series(page)


@router.get("/games")
async def discover_games(
    page: int = Query(1),
    _current_user: int = Depends(get_current_user_id),
):
    return await get_popular_games(page)


@router.get("/search")
async def search(
    q: str = Query(...),
    page: int = Query(1),
    _current_user: int = Depends(get_current_user_id),
):
    if not q or not q.strip():
        raise HTTPException(status_code=400, detail="El parametro 'q' es obligatorio")
    return await search_all(q, page)


@router.get("/search/movies")
async def search_movies_endpoint(
    q: str = Query(...),
    page: int = Query(1),
    _current_user: int = Depends(get_current_user_id),
):
    if not q or not q.strip():
        raise HTTPException(status_code=400, detail="El parametro 'q' es obligatorio")
    return await search_movies_and_series(q, page)


@router.get("/search/games")
async def search_games_endpoint(
    q: str = Query(...),
    page: int = Query(1),
    _current_user: int = Depends(get_current_user_id),
):
    if not q or not q.strip():
        raise HTTPException(status_code=400, detail="El parametro 'q' es obligatorio")
    return await search_games(q, page)
