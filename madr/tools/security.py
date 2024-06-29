from datetime import datetime, timedelta, timezone

import jwt
from fastapi import HTTPException, status

from madr.infra import config

CredentialException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail='Invalid credentials',
    headers={'WWW-Authenticate': 'Bearer'},
)


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(tz=timezone.utc) + timedelta(
        minutes=config.AUTH_JWT_EXPIRES_MINUTES
    )
    to_encode.update({'exp': expire})
    return jwt.encode(
        to_encode, config.AUTH_SECRET_KEY, algorithm=config.AUTH_ALGORITHM
    )


def get_payload_from_token(token: str):
    if not token:
        raise CredentialException
    try:
        payload: dict = jwt.decode(
            token, config.AUTH_SECRET_KEY, algorithms=[config.AUTH_ALGORITHM]
        )
        p = payload.copy()
        p.pop('exp')
        if p.values():
            return payload
        raise CredentialException
    except jwt.DecodeError as e:
        raise CredentialException
