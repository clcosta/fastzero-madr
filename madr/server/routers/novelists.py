from typing import Annotated

from fastapi import APIRouter, Depends, Query, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from madr.database.database import get_session
from madr.database.models import User
from madr.server.schemas.base import Message
from madr.server.schemas.novelist import (
    GetManyNovelistsResponseSchema,
    NovelistRequestSchema,
    NovelistResponseSchema,
)
from madr.server.services.auth_service import get_current_user
from madr.server.services.novelist_service import (
    create_novelist_service,
    delete_novelist_service,
    get_novelist_service,
    get_novelists_service,
    update_novelist_service,
)

router = APIRouter(
    prefix='/romancistas',
    tags=['Romancistas'],
)

DBSession = Annotated[Session, Depends(get_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]


@router.post(
    '/romancista',
    status_code=status.HTTP_201_CREATED,
    response_model=NovelistResponseSchema,
)
def create_novelist(
    data: NovelistRequestSchema, current_user: CurrentUser, db: DBSession
):
    novelist = create_novelist_service(data, db)
    return NovelistResponseSchema(
        id=novelist.id,
        nome=novelist.name,
    )


@router.delete('/romancista/{id}', status_code=status.HTTP_200_OK)
def delete_novelist(id: int, current_user: CurrentUser, db: DBSession):
    delete_novelist_service(id, db)
    return Message(message='Romancista deletado no MADR')


@router.patch(
    '/romancista/{id}',
    status_code=status.HTTP_200_OK,
    response_model=NovelistResponseSchema,
)
def update_novelist(
    id: int,
    data: NovelistRequestSchema,
    current_user: CurrentUser,
    db: DBSession,
):
    novelist = update_novelist_service(id, data, db)
    return NovelistResponseSchema(
        id=novelist.id,
        nome=novelist.name,
    )


@router.get(
    '/romancista/{id}',
    status_code=status.HTTP_200_OK,
    response_model=NovelistResponseSchema,
)
def get_novelist(id: int, db: DBSession):
    novelist = get_novelist_service({'id': id}, db)
    return NovelistResponseSchema(
        id=novelist.id,
        nome=novelist.name,
    )


@router.get(
    '/romancista',
    status_code=status.HTTP_200_OK,
    response_model=GetManyNovelistsResponseSchema,
)
def get_novelists(
    db: DBSession,
    name: str | None = Query(None, alias='nome'),
    page: int = 1,
):
    where = {
        'name': name,
    }
    novelists = get_novelists_service(where, db, page)
    return GetManyNovelistsResponseSchema(
        romancistas=[
            NovelistResponseSchema(
                id=novelist.id,
                nome=novelist.name,
            )
            for novelist in novelists
        ]
    )
