from sqlalchemy import Integer, Enum
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base
from app.models.swipe import SwipeState


class PeopleSwipe(Base):
    __tablename__ = "PeopleSwipe"

    Id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    UserId: Mapped[int] = mapped_column(Integer)
    MatchingUserId: Mapped[int] = mapped_column(Integer)
    State: Mapped[SwipeState] = mapped_column(Enum(SwipeState))
