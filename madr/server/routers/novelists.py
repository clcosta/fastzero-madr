from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse

router = APIRouter(
    prefix='/romancistas',
    tags=['Romancistas'],
)  # PROTECT ROUTER


@router.post('/romancista', status_code=status.HTTP_201_CREATED)
def create_novelist():
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={'message': 'Romancista criado com sucesso!'},
    )


@router.delete('/romancista/{id}', status_code=status.HTTP_200_OK)
def delete_novelist(id: int):
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={'message': f'Romancista {id} deletado com sucesso!'},
    )


@router.patch('/romancista/{id}', status_code=status.HTTP_200_OK)
def update_novelist(id: int):
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={'message': f'Romancista {id} atualizado com sucesso!'},
    )


@router.get('/romancista/{id}', status_code=status.HTTP_200_OK)
def get_novelist(id: int):
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={'message': f'Romancista {id} retornado com sucesso!'},
    )


@router.get('/romancista', status_code=status.HTTP_200_OK)
def get_novelists():
    ## Here could be use params to filter
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={'message': 'Romancistas retornados com sucesso!'},
    )
