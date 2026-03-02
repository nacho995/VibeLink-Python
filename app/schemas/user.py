from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    avatar_url: Optional[str] = None
    codigo_invitacion: Optional[str] = None
    fecha_registro: datetime
    gender: str
    date_of_birth: datetime
    bio: Optional[str] = None
    is_premium: bool
    swipes: int

    model_config = {"from_attributes": True}


class ProfileUpdateDTO(BaseModel):
    avatar_url: Optional[str] = None
    gender: str
    date_of_birth: datetime
    bio: Optional[str] = None
