from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse

router = APIRouter(
    prefix='/contas',
    tags=['Contas'],
)


@router.post('/conta', status_code=status.HTTP_201_CREATED)
def create_account():
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={'message': 'Conta criada com sucesso!'},
    )


@router.put('/conta/{id}', status_code=status.HTTP_200_OK)
def update_account(id: int):
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={'message': f'Conta {id} atualizada com sucesso!'},
    )


@router.delete('/conta/{id}', status_code=status.HTTP_200_OK)
def delete_account(id: int):
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={'message': f'Conta {id} deletada com sucesso!'},
    )


@router.post('/token', status_code=status.HTTP_200_OK)
def create_token():
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={'message': 'Token criado com sucesso!'},
    )


@router.post('/refresh-token', status_code=status.HTTP_200_OK)
def refresh_token():
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={'message': 'Token atualizado com sucesso!'},
    )
