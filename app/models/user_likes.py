import enum

from sqlalchemy import Integer, Enum
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class LikeState(enum.Enum):
    Liked = "Liked"
    Disliked = "Disliked"


class UserLikes(Base):
    __tablename__ = "UserLikes"

    Id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    UserId: Mapped[int] = mapped_column(Integer)
    ContentId: Mapped[int] = mapped_column(Integer)
    Punctuation: Mapped[int] = mapped_column(Integer, default=0)
    State: Mapped[LikeState] = mapped_column(Enum(LikeState), default=LikeState.Liked)
