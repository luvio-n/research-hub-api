from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(255), unique=True)
    materials: Mapped[list["Material"]] = relationship(back_populates="user")

class Topic(Base):
    __tablename__ = "topics"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    description: Mapped[str | None] = mapped_column(String(500), nullable=True)

class Material(Base):
    __tablename__ = "materials"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(255))
    type: Mapped[str] = mapped_column(String(50))
    author: Mapped[str | None] = mapped_column(String(255), nullable=True)
    source: Mapped[str | None] = mapped_column(String(255), nullable=True)
    url: Mapped[str | None] = mapped_column(String(2048), nullable=True)

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped["User"] = relationship(back_populates="materials")
    topic_id: Mapped[int] = mapped_column(ForeignKey("topics.id"))

    description: Mapped[str | None] = mapped_column(nullable=True)
    main_idea: Mapped[str | None] = mapped_column(nullable=True)
    interesting: Mapped[str | None] = mapped_column(nullable=True)
    connections: Mapped[str | None] = mapped_column(nullable=True)
    questions: Mapped[str | None] = mapped_column(nullable=True)
    tags: Mapped[list["MaterialTag"]] = relationship(back_populates="material")

class Tag(Base):
    __tablename__ = "tags"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True)
    material_tags: Mapped[list["MaterialTag"]] = relationship(back_populates="tag")

class MaterialTag(Base):
    __tablename__ = "material_tags"

    material_id: Mapped[int] = mapped_column(
        ForeignKey("materials.id"),
        primary_key=True,
    )
    tag_id: Mapped[int] = mapped_column(
        ForeignKey("tags.id"),
        primary_key=True,
    )
    material: Mapped["Material"] = relationship(back_populates="tags")
    tag: Mapped["Tag"] = relationship(back_populates="material_tags")