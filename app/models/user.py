import enum
from datetime import datetime, timezone

from sqlalchemy import String, Boolean, Integer, DateTime, Enum
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class Gender(enum.Enum):
    Male = "Male"
    Female = "Female"


class User(Base):
    __tablename__ = "Users"

    Id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    Username: Mapped[str] = mapped_column(String, default="")
    Email: Mapped[str] = mapped_column(String, default="")
    PasswordHash: Mapped[str] = mapped_column(String, default="")
    AvatarUrl: Mapped[str | None] = mapped_column(String, nullable=True)
    CodigoInvitacion: Mapped[str | None] = mapped_column(String, nullable=True)
    FechaRegistro: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
    Gender: Mapped[Gender] = mapped_column(Enum(Gender), default=Gender.Male)
    DateOfBirth: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
    Bio: Mapped[str | None] = mapped_column(String, nullable=True)
    IsPremium: Mapped[bool] = mapped_column(Boolean, default=False)
    Swipes: Mapped[int] = mapped_column(Integer, default=0)
    LastSwipeUpdate: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
