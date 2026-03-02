import enum

from sqlalchemy import String, Integer, Enum, ARRAY
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class ContentType(enum.Enum):
    pelicula = "pelicula"
    serie = "serie"
    videojuego = "videojuego"


class Content(Base):
    __tablename__ = "Content"

    Id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    Type: Mapped[ContentType] = mapped_column(Enum(ContentType))
    ApiId: Mapped[int] = mapped_column(Integer)
    Titulo: Mapped[str] = mapped_column(String, default="")
    ImagenUrl: Mapped[str | None] = mapped_column(String, nullable=True)
    Generos: Mapped[list[str] | None] = mapped_column(ARRAY(String), nullable=True)
    Año: Mapped[int] = mapped_column(Integer, default=0, name="Año")
