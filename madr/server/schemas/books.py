from pydantic import BaseModel, Field


class BaseBook(BaseModel):
    year: int = Field(alias='ano')
    title: str = Field(alias='titulo')
    novelist_id: int = Field(alias='romancista_id')


class CreateBookRequestSchema(BaseBook):
    pass


class CreateBookResponseSchema(BaseBook):
    id: int


class UpdateBookRequestSchema(BaseModel):
    year: int


class UpdateBookResponseSchema(BaseBook):
    pass


class GetBookResponseSchema(BaseBook):
    id: int


class GetManyBooksResponseSchema(BaseModel):
    books: list[GetBookResponseSchema] = Field(alias='livros')
