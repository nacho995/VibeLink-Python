from typing import Optional

from pydantic import BaseModel


class SwipeDTO(BaseModel):
    user_id: int
    content_id: int = 0
    matching_user_id: int = 0
    state: str = "Liked"
    punctuation: int = 0


class ExternalLikeDTO(BaseModel):
    user_id: int
    external_id: str
    title: str
    image_url: Optional[str] = None
    state: str = "Liked"


class PeopleSwipeDTO(BaseModel):
    user_id: int
    matching_user_id: int
    state: str  # "Like" or "Dislike"
