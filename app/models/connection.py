import enum
from datetime import datetime, timezone

from sqlalchemy import Integer, DateTime, Enum
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class ConnectionState(enum.Enum):
    Pendiente = "Pendiente"
    Aceptado = "Aceptado"
    Rechazado = "Rechazado"
    Bloqueado = "Bloqueado"


class Connection(Base):
    __tablename__ = "Conections"

    Id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    UserId: Mapped[int] = mapped_column(Integer)
    FriendId: Mapped[int] = mapped_column(Integer)
    State: Mapped[ConnectionState] = mapped_column(Enum(ConnectionState))
    Date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
