from typing import Annotated

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from madr.database.models import User
from madr.server.schemas.base import Message
from madr.server.schemas.books import (
    CreateBookRequestSchema,
    CreateBookResponseSchema,
    GetBookResponseSchema,
    GetManyBooksResponseSchema,
    UpdateBookRequestSchema,
)
from madr.server.services.auth_service import get_current_user, get_session
from madr.server.services.book_service import (
    create_book_service,
    delete_book_service,
    get_book_service,
    get_books_service,
    update_book_service,
)

router = APIRouter(
    prefix='/livros',
    tags=['Livros'],
)

DBSession = Annotated[Session, Depends(get_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]


@router.post(
    '/livro',
    status_code=status.HTTP_200_OK,
    response_model=CreateBookResponseSchema,
)
def create_book(
    data: CreateBookRequestSchema, current_user: CurrentUser, db: DBSession
):
    book = create_book_service(data, db)
    return book


@router.delete('/livro/{id}', status_code=status.HTTP_200_OK)
def delete_book(id: int, current_user: CurrentUser, db: DBSession):
    delete_book_service(id, db)
    return Message(message='Livro deletado no MADR')


@router.patch(
    '/livro/{id}',
    status_code=status.HTTP_200_OK,
    response_model=UpdateBookRequestSchema,
)
def update_book(
    id: int,
    data: UpdateBookRequestSchema,
    current_user: CurrentUser,
    db: DBSession,
):
    new_book = update_book_service(id, data, db)
    return new_book


@router.get(
    '/livro/{id}',
    status_code=status.HTTP_200_OK,
    response_model=GetBookResponseSchema,
)
def get_book(id: int, db: DBSession):
    book = get_book_service({'id': id}, db=db)
    return book


@router.get(
    '/livro',
    status_code=status.HTTP_200_OK,
    response_model=GetManyBooksResponseSchema,
)
def get_books(
    db: DBSession,
    year: int | None = Query(None, alias='ano'),
    name: str | None = Query(None, alias='nome'),
    page: int = Query(1, alias='pagina'),
):
    where = {}
    if year:
        where['year'] = year
    if name:
        where['title']
    books = get_books_service(where, db, page)
    books = [
        GetBookResponseSchema(
            id=book.id,
            ano=book.year,
            titulo=book.title,
            romancista_id=book.author_id,
        )
        for book in books
    ]
    return GetManyBooksResponseSchema(livros=books)
