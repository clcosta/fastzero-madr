from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from .routers import accounts, books, novelists

app = FastAPI()

app.include_router(accounts.router)
app.include_router(books.router)
app.include_router(novelists.router)


@app.get('/', include_in_schema=False)
def redirect_to_swagger():
    return RedirectResponse(url='/docs')
