from http import HTTPStatus

from fastapi.testclient import TestClient

from madr.database.models import User


class TestAuth:
    def test_login(self, client: TestClient, user: User):
        login = {
            'username': user.email,
            'password': user.clean_password,
        }
        response = client.post('/contas/token', data=login)
        assert response.status_code == HTTPStatus.OK
        assert 'access_token' in response.json()

    def test_login_invalid_user(self, client: TestClient, user: User):
        login = {
            'username': 'mistermonk@police.com',
            'password': 'trudy',
        }
        response = client.post('/contas/token', data=login)
        assert response.status_code == HTTPStatus.BAD_REQUEST

    def test_login_invalid_password(self, client: TestClient, user: User):
        login = {'username': user.email, 'password': 'ABC'}
        response = client.post('/contas/token', data=login)
        assert response.status_code == HTTPStatus.BAD_REQUEST

    def test_refresh_token(self, client: TestClient, token: str):
        response = client.post(
            '/contas/refresh-token',
            headers={'Authorization': f'Bearer {token}'},
        )
        assert response.status_code == HTTPStatus.OK
        assert 'access_token' in response.json()
