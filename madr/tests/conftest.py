import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from madr.database import get_session
from madr.database.models import User, table_registry
from madr.server import app
from madr.tools.hash import hash_pwd


@pytest.fixture()
def client(session: Session):
    def get_session_override():
        return session

    with TestClient(app) as client:
        app.dependency_overrides[get_session] = get_session_override
        yield client

    app.dependency_overrides.clear()


@pytest.fixture()
def session():
    engine = create_engine(
        'sqlite:///:memory:',
        connect_args={'check_same_thread': False},
        poolclass=StaticPool,
    )
    table_registry.metadata.create_all(engine)

    with Session(engine) as session:
        yield session

    table_registry.metadata.drop_all(engine)


@pytest.fixture()
def user(session: Session):
    user = User(
        username='Teste',
        email='teste@test.com',
        password=hash_pwd('testtest'),
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    user.clean_password = 'testtest'
    return user


@pytest.fixture()
def token(client: TestClient, user: User):
    response = client.post(
        '/contas/token',
        data={'username': user.email, 'password': user.clean_password},
    )
    return response.json()['access_token']
