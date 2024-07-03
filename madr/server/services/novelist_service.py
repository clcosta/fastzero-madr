from typing import TypedDict

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from madr.database.models import Novelists
from madr.server.schemas.novelist import NovelistRequestSchema
from madr.tools.sanitize import sanitize_str

NovelistNotFound = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail='Romancista não encontrado no MADR',
)


class NovelistWhere(TypedDict, total=False):
    id: int
    name: str


def create_novelist_service(data: NovelistRequestSchema, db: Session):
    novelist = Novelists(name=sanitize_str(data.name))

    if db.scalar(select(Novelists).filter(Novelists.name == novelist.name)):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='Romancista já consta no MADR',
        )
    db.add(novelist)
    db.commit()
    db.refresh(novelist)
    return novelist


def delete_novelist_service(id: int, db: Session):
    novelist = db.get(Novelists, id)
    if not novelist:
        raise NovelistNotFound
    db.delete(novelist)
    db.commit()
    return


def update_novelist_service(id: int, data: NovelistRequestSchema, db: Session):
    novelist = db.get(Novelists, id)
    if not novelist:
        raise NovelistNotFound
    novelist.name = sanitize_str(data.name)
    db.commit()
    db.refresh(novelist)
    return novelist


def get_novelist_service(where: NovelistWhere, db: Session):
    if not where:
        return None   # pragma: no cover
    novelist = db.scalar(select(Novelists).filter_by(**where))
    if not novelist:
        raise NovelistNotFound
    return novelist


def get_novelists_service(where: NovelistWhere, db: Session, page: int = 1):
    if not where:
        return []  # pragma: no cover
    query = (
        select(Novelists).filter_by(**where).limit(20).offset((page - 1) * 20)
    )
    name = where.pop('name', None)
    if name:
        name = sanitize_str(name)
        query = (
            select(Novelists)
            .filter(Novelists.name.like(f'%{name}%'))
            .limit(20)
            .offset((page - 1) * 20)
        )

    novelists = db.scalars(query).all()
    return novelists
