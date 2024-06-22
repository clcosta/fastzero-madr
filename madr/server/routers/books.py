from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse

router = APIRouter(
    prefix='/livros',
    tags=['Livros'],
)  # PROTECT ROUTER


@router.post('/livro', status_code=status.HTTP_200_OK)
def create_book():
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={'message': 'Livro criado com sucesso!'},
    )


@router.delete('/livro/{id}', status_code=status.HTTP_200_OK)
def delete_book(id: int):
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={'message': f'Livro {id} deletado com sucesso!'},
    )


@router.patch('/livro/{id}', status_code=status.HTTP_200_OK)
def update_book(id: int):
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={'message': f'Livro {id} atualizado com sucesso!'},
    )


@router.get('/livro/{id}', status_code=status.HTTP_200_OK)
def get_book(id: int):
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={'message': f'Livro {id} retornado com sucesso!'},
    )


@router.get('/livro', status_code=status.HTTP_200_OK)
def get_books():
    ## Here could be use params to filter
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={'message': 'Livros retornados com sucesso!'},
    )
