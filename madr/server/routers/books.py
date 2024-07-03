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
    status_code=status.HTTP_201_CREATED,
    response_model=CreateBookResponseSchema,
)
def create_book(
    data: CreateBookRequestSchema, current_user: CurrentUser, db: DBSession
):
    book = create_book_service(data, db)
    return CreateBookResponseSchema(
        id=book.id,
        ano=book.year,
        titulo=book.title,
        romancista_id=book.author_id,
    )


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
    return UpdateBookRequestSchema(
        id=new_book.id,
        ano=new_book.year,
        titulo=new_book.title,
        romancista_id=new_book.author_id,
    )


@router.get(
    '/livro/{id}',
    status_code=status.HTTP_200_OK,
    response_model=GetBookResponseSchema,
)
def get_book(id: int, db: DBSession):
    book = get_book_service({'id': id}, db=db)
    return GetBookResponseSchema(
        id=book.id,
        ano=book.year,
        titulo=book.title,
        romancista_id=book.author_id,
    )


@router.get(
    '/livro',
    status_code=status.HTTP_200_OK,
    response_model=GetManyBooksResponseSchema,
)
def get_books(
    db: DBSession,
    year: int | None = Query(None, alias='ano'),
    title: str | None = Query(None, alias='titulo'),
    page: int = Query(1, alias='pagina'),
):
    where = {}
    if year:
        where['year'] = year
    if title:
        where['title'] = title
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
