from datetime import datetime, timezone

from sqlalchemy import Integer, String, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class MessageChat(Base):
    __tablename__ = "MessageChats"

    Id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    UserId: Mapped[int] = mapped_column(Integer)
    MatchingUserId: Mapped[int] = mapped_column(Integer)
    Message: Mapped[str] = mapped_column(String, default="")
    Date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
