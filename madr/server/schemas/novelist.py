from pydantic import BaseModel, Field, field_validator


class BaseNovelist(BaseModel):
    name: str = Field(alias='nome')


class NovelistRequestSchema(BaseNovelist):
    @field_validator('name')
    @classmethod
    def name_must_not_be_empty(cls, value: str) -> str:
        if not value:
            raise ValueError('Nome do romancista não pode ser vazio')
        return value


class NovelistResponseSchema(BaseNovelist):
    id: int


class GetManyNovelistsResponseSchema(BaseModel):
    romancistas: list[NovelistResponseSchema] = Field(alias='romancistas')
