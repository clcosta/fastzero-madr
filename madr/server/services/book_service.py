from typing import TypedDict

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from madr.database.models import Book, Novelists
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

    book.year = data.year
    db.commit()
    db.refresh(book)
    return book


def get_books_service(where: BookWhere, db: Session, page: int = 1):
    if not where:
        return []
    title = where.pop('title', None)
    query = select(Book).filter_by(**where).limit(20).offset((page - 1) * 20)
    if title:
        title = sanitize_str(title)
        query = (
            select(Book)
            .filter_by(**where)
            .where(Book.title.like(f'%{title}%'))
            .limit(20)
            .offset((page - 1) * 20)
        )
    books = db.scalars(query).all()
    return books


def get_book_service(where: BookWhere, db: Session) -> Book:
    if not where:
        return None
    book = db.scalar(select(Book).filter_by(**where))
    if not book:
        raise BookNotFound
    return book
