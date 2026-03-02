from typing import Optional

from pydantic import BaseModel


class ContentItemResponse(BaseModel):
    external_id: str = ""
    title: str = ""
    type: str = ""
    image_url: Optional[str] = None
    backdrop_url: Optional[str] = None
    description: str = ""
    rating: float = 0.0
    year: Optional[int] = None
    genres: list[str] = []
    platforms: Optional[list[str]] = None


class ContentDiscoveryResponse(BaseModel):
    movies: list[ContentItemResponse] = []
    series: list[ContentItemResponse] = []
    games: list[ContentItemResponse] = []
