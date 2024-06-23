from typing import Annotated

from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from madr.database import get_session
from madr.database.models import User
from madr.server.schemas.accounts import (
    AccountRequestSchema,
    AccountResponseSchema,
)
from madr.server.schemas.auth import TokenSchema
from madr.server.schemas.base import Message
from madr.server.services.account_service import (
    delete_user,
    register_user,
    update_user,
)
from madr.server.services.auth_service import auth_service, get_current_user

router = APIRouter(
    prefix='/contas',
    tags=['Contas'],
)

DBSession = Annotated[Session, Depends(get_session)]
AuthForm = Annotated[OAuth2PasswordRequestForm, Depends()]
CurrentUser = Annotated[User, Depends(get_current_user)]


@router.post(
    '/conta',
    status_code=status.HTTP_201_CREATED,
    response_model=AccountResponseSchema,
)
def create_account(account: AccountRequestSchema, db: DBSession):
    user = register_user(account, db)
    return user


@router.put(
    '/conta/{id}',
    status_code=status.HTTP_200_OK,
    response_model=AccountResponseSchema,
)
def update_account(
    id: int,
    account: AccountRequestSchema,
    current_user: CurrentUser,
    db: DBSession,
):
    updated_user = update_user(id, account, db, current_user)
    return updated_user


@router.delete(
    '/conta/{id}', status_code=status.HTTP_200_OK, response_model=Message
)
def delete_account(id: int, current_user: CurrentUser, db: DBSession):
    delete_user(id, db, current_user)
    return Message(message='Conta deletada com sucesso!')


@router.post(
    '/token', status_code=status.HTTP_200_OK, response_model=TokenSchema
)
def create_token(form: AuthForm, db: DBSession):
    token = auth_service(form, db)
    return token


@router.post('/refresh-token', status_code=status.HTTP_200_OK)
def refresh_token():
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={'message': 'Token atualizado com sucesso!'},
    )
