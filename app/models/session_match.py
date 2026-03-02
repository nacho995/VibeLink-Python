from datetime import datetime, timezone

from sqlalchemy import Integer, DateTime, Enum
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base
from app.models.content import ContentType


class SessionMatch(Base):
    __tablename__ = "SessionMatches"

    Id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    UserId: Mapped[int] = mapped_column(Integer)
    FriendId: Mapped[int] = mapped_column(Integer)
    Type: Mapped[ContentType] = mapped_column(Enum(ContentType))
    Date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
