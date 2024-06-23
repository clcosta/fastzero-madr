from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from madr.database.models import User
from madr.server.schemas.accounts import AccountRequestSchema
from madr.tools import hash, sanitize


def register_user(account: AccountRequestSchema, db: Session):
    existent_user = db.scalar(
        select(User).where(
            (User.username == account.username) | (User.email == account.email)
        )
    )
    if existent_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='Conta já consta no MADR',
        )
    pwd = hash.hash_pwd(account.password)
    username = sanitize.sanitize_str(account.username)
    user = User(username=username, email=account.email, password=pwd)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def update_user(
    id: int, account: AccountRequestSchema, db: Session, current_user: User
):
    user = db.get(User, id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Conta não encontrada',
        )
    if user.id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Usuário não tem permissão para alterar esta conta',
        )
    user.username = sanitize.sanitize_str(account.username)
    user.email = account.email
    user.password = hash.hash_pwd(account.password)
    db.commit()
    db.refresh(user)
    return user


def delete_user(id: int, db: Session, current_user: User):
    user = db.get(User, id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Conta não encontrada',
        )
    if user.id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Usuário não tem permissão para deletar esta conta',
        )
    db.delete(user)
    db.commit()
    return user
