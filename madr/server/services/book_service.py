from typing import TypedDict

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from madr.database.models import Book
from madr.server.schemas.books import (
    CreateBookRequestSchema,
    UpdateBookRequestSchema,
)
from madr.tools.sanitize import sanitize_str

BookNotFound = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail='Livro não encontrado',
)


class BookWhere(TypedDict, total=False):
    id: int
    title: str
    year: int
    novelist: int


def create_book_service(data: CreateBookRequestSchema, db: Session) -> Book:
    book = Book(
        title=data.title,
        year=data.year,
        author_id=data.novelist_id,
    )
    book.title = sanitize_str(book.title)

    if db.scalar(select(Book).filter(Book.title == book.title)):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='Livro já cadastrado',
        )

    db.add(book)
    db.commit()
    db.refresh(book)
    return book


def delete_book_service(id: int, db: Session) -> Book:
    book = db.get(Book, id)
    if not book:
        raise BookNotFound

    db.delete(book)
    db.commit()
    return book


def update_book_service(
    id: int, data: UpdateBookRequestSchema, db: Session
) -> Book:
    book = db.get(Book, id)
    if not book:
        raise BookNotFound

    if book.title == sanitize_str(data.title):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='Livro já cadastrado no MADR',
        )
    book.year = data.year
    book.title = sanitize_str(data.title)
    book.author_id = data.novelist_id
    db.commit()
    db.refresh(book)
    return book


def get_books_service(where: BookWhere, db: Session, page: int = 1):
    if not where:
        return []  # pragma: no cover
    query = select(Book).filter_by(**where).limit(20).offset((page - 1) * 20)
    title = where.pop('title', None)
    if title:
        title = sanitize_str(title)
        query = (
            select(Book)
            .filter(Book.title.like(f'%{title}%'))
            .limit(20)
            .offset((page - 1) * 20)
        )

    novelists = db.scalars(query).all()
    return novelists


def get_book_service(where: BookWhere, db: Session) -> Book:
    if not where:
        return None  # pragma: no cover
    book = db.scalar(select(Book).filter_by(**where))
    if not book:
        raise BookNotFound
    return book
