from datetime import datetime

from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, registry, relationship

table_registry = registry()


@table_registry.mapped_as_dataclass
class User:
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    email: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(
        init=False,
        server_default=func.now(),
    )


@table_registry.mapped_as_dataclass
class Book:
    __tablename__ = 'books'
    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    title: Mapped[str] = mapped_column(unique=True)
    year: Mapped[str]
    author_id: Mapped[int] = mapped_column(ForeignKey('novelists.id'))
    author: Mapped['Novelists'] = relationship(
        init=False,
        back_populates='books',
    )
    created_at: Mapped[datetime] = mapped_column(
        init=False,
        server_default=func.now(),
    )


@table_registry.mapped_as_dataclass
class Novelists:
    __tablename__ = 'novelists'
    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)
    books: Mapped[list[Book]] = relationship(
        init=False,
        back_populates='author',
        cascade='all, delete-orphan',
    )
    created_at: Mapped[datetime] = mapped_column(
        init=False,
        server_default=func.now(),
    )
