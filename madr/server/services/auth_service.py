from typing import Annotated

from fastapi import Depends, Header, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.orm import Session

from madr.database import get_session
from madr.database.models import User
from madr.tools import hash, security

AuthForm = Annotated[OAuth2PasswordRequestForm, Depends()]
DBSession = Annotated[Session, Depends(get_session)]

AuthException = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST, detail='Email ou senha incorretos'
)

InvalidCredentialsException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail='Não autorizado',
    headers={'WWW-Authenticate': 'Bearer'},
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='contas/token')


def auth_service(form: AuthForm, db: Session):
    user = db.scalar(select(User).where(User.email == form.username))
    if not user:
        raise AuthException

    if not hash.check_pwd(form.password, user.password):
        raise AuthException

    access_token = security.create_access_token({'sub': user.email})
    return {'access_token': access_token, 'token_type': 'bearer'}


async def get_current_user(db: DBSession, token: str = Depends(oauth2_scheme)):
    if not token:
        raise InvalidCredentialsException
    payload = security.get_payload_from_token(token)
    username: str = payload.get('sub')
    if not username:
        raise InvalidCredentialsException
    user = db.scalar(select(User).where(User.email == username))
    if user is None:
        raise InvalidCredentialsException
    return user
