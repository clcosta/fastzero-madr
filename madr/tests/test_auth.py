from datetime import datetime, timedelta
from http import HTTPStatus

from fastapi.testclient import TestClient
from freezegun import freeze_time

from madr.database.models import User
from madr.infra import config
from madr.tools import security


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

    def test_refresh_token_user_not_longer_exists(
        self, client: TestClient, deleted_user_token: str
    ):
        response = client.post(
            '/contas/refresh-token',
            headers={'Authorization': f'Bearer {deleted_user_token}'},
        )

        assert response.status_code == HTTPStatus.UNAUTHORIZED

    def test_token_expired_after_time(self, client: TestClient, user: User):
        today_expire = datetime.now()
        with freeze_time(today_expire.strftime('%Y-%m-%d %H:%M:%S')):
            login = {
                'username': user.email,
                'password': user.clean_password,
            }
            response = client.post('/contas/token', data=login)
            assert response.status_code == HTTPStatus.OK
            assert 'access_token' in response.json()

            access_token = response.json()['access_token']

        today_expire = today_expire + timedelta(
            minutes=config.AUTH_JWT_EXPIRES_MINUTES + 1
        )
        with freeze_time(today_expire.strftime('%Y-%m-%d %H:%M:%S')):
            response = client.post(
                '/contas/refresh-token',
                headers={'Authorization': f'Bearer {access_token}'},
            )
            assert response.status_code == HTTPStatus.UNAUTHORIZED

    def test_get_current_user_without_token(self, client: TestClient):
        response = client.post(
            '/contas/refresh-token', headers={'Authorization': 'Bearer '}
        )
        assert response.status_code == HTTPStatus.UNAUTHORIZED

    def test_get_current_user_with_invalid_token(self, client: TestClient):
        token = security.create_access_token({})
        response = client.post(
            '/contas/refresh-token',
            headers={'Authorization': f'Bearer {token}'},
        )
        assert response.status_code == HTTPStatus.UNAUTHORIZED

    def test_get_current_user_with_deleted_user_token(
        self, client: TestClient, deleted_user_token: str
    ):
        response = client.post(
            '/contas/refresh-token',
            headers={'Authorization': f'Bearer {deleted_user_token}'},
        )
        assert response.status_code == HTTPStatus.UNAUTHORIZED
