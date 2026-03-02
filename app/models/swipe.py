import enum

from sqlalchemy import Integer, Enum
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class SwipeState(enum.Enum):
    Like = "Like"
    Dislike = "Dislike"


class Swipe(Base):
    __tablename__ = "Swipes"

    Id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    UserId: Mapped[int] = mapped_column(Integer)
    MatchingUserId: Mapped[int] = mapped_column(Integer)
    State: Mapped[SwipeState] = mapped_column(Enum(SwipeState))
