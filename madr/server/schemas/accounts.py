from pydantic import BaseModel, EmailStr, Field


class AccountRequestSchema(BaseModel):
    username: str = Field(..., serialization_alias='username')
    email: EmailStr = Field(..., serialization_alias='email')
    password: str = Field(..., alias='senha', serialization_alias='senha')


class AccountResponseSchema(BaseModel):
    id: int = Field(..., serialization_alias='id')
    username: str = Field(..., serialization_alias='username')
    email: EmailStr = Field(..., serialization_alias='email')
