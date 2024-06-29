import random
import string
from http import HTTPStatus

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from madr.database.models import User
from madr.tools.hash import is_hashed_pwd


class TestCreateUser:
    def test_create_user(self, client: TestClient):
        user = {
            'username': 'fausto',
            'email': 'fausto@fausto.com',
            'senha': '1234567',
        }
        response = client.post('/contas/conta', json=user)
        assert response.status_code == HTTPStatus.CREATED
        res_json = response.json()
        expected_keys = ['username', 'email', 'id']
        assert sorted(list(res_json.keys())) == sorted(expected_keys)
        assert res_json['username'] == user['username']
        assert res_json['email'] == user['email']
        assert res_json['id'] > 0

    def test_create_user_hash_passowrd(
        self, client: TestClient, session: Session
    ):
        user = {
            'username': 'ABC',
            'email': 'abc@abc.com',
            'senha': '1234567',
        }
        response = client.post('/contas/conta', json=user)
        assert response.status_code == HTTPStatus.CREATED
        db_user = session.query(User).filter_by(email=user['email']).first()
        assert db_user.password != user['senha']
        assert is_hashed_pwd(db_user.password)

    def test_create_user_invalid_data(self, client: TestClient):
        user = {
            'username': 'fausto',
            'email': 'BATATA-FRITA',
            'senha': '1234567',
        }
        response = client.post('/contas/conta', json=user)
        assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY

    def test_create_user_missing_data(self, client: TestClient):
        user = {
            'username': 'fausto',
            'senha': '1234567',
        }
        response = client.post('/contas/conta', json=user)
        assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY

    def test_create_user_already_exists(self, client: TestClient):
        user = {
            'username': 'edgar',
            'email': 'edgar@edgar.com',
            'senha': '1234567',
        }
        response = client.post('/contas/conta', json=user)
        assert response.status_code == HTTPStatus.CREATED
        response = client.post('/contas/conta', json=user)
        assert response.status_code == HTTPStatus.CONFLICT


class TestUpdateUser:
    def test_update_user(self, client: TestClient, user: User, token: str):
        random_email = (
            ''.join(random.choices(string.ascii_letters, k=10)) + '@email.com'
        )
        while random_email == user.email:
            random_email = (
                random.choices(string.ascii_letters, k=10) + '@email.com'
            )  # pragma: no cover
        old_email = user.email
        response = client.put(
            f'/contas/conta/{user.id}',
            headers={'Authorization': f'Bearer {token}'},
            json={
                'username': user.username,
                'email': random_email,
                'senha': 'newPassword',
            },
        )
        assert response.status_code == HTTPStatus.OK
        res_json = response.json()
        assert res_json['username'] == user.username
        assert res_json['email'] == random_email
        assert res_json['email'] != old_email
        assert res_json['id'] == user.id

    def test_update_user_invalid_user_id(
        self, client: TestClient, user: User, token: str
    ):
        response = client.put(
            f'/contas/conta/0',
            headers={'Authorization': f'Bearer {token}'},
            json={
                'username': user.username,
                'email': user.email,
                'senha': '123',
            },
        )
        assert response.status_code == HTTPStatus.NOT_FOUND

    def test_update_another_user(
        self, client: TestClient, user: User, token: str
    ):
        new_account = {
            'username': 'new_user',
            'email': 'new_user@email.com',
            'senha': '1234567',
        }
        response = client.post('/contas/conta', json=new_account)
        assert response.status_code == HTTPStatus.CREATED
        new_account_json = response.json()
        new_id = new_account_json['id']
        response = client.put(
            f'/contas/conta/{new_id}',
            headers={'Authorization': f'Bearer {token}'},
            json={
                'username': user.username,
                'email': user.email,
                'senha': '123',
            },
        )
        assert response.status_code == HTTPStatus.UNAUTHORIZED


class TestDeleteUser:
    def test_delete_user(self, client: TestClient, token: str):
        to_delete = {
            'username': 'faustao',
            'email': 'fausto_e_selena@email.com',
            'senha': '1234567',
        }
        response = client.post('/contas/conta', json=to_delete)
        assert response.status_code == HTTPStatus.CREATED
        user_to_delete = response.json()
        response = client.post(
            '/contas/token',
            data={
                'username': to_delete['email'],
                'password': to_delete['senha'],
            },
        )
        assert response.status_code == HTTPStatus.OK
        to_delete_token = response.json()['access_token']
        response = client.delete(
            f'/contas/conta/{user_to_delete["id"]}',
            headers={'Authorization': f'Bearer {to_delete_token}'},
        )
        assert response.status_code == HTTPStatus.OK

    def test_delete_user_invalid_user_id(
        self, client: TestClient, user: User, token: str
    ):
        response = client.delete(
            f'/contas/conta/0',
            headers={'Authorization': f'Bearer {token}'},
        )
        assert response.status_code == HTTPStatus.NOT_FOUND

    def test_delete_another_user(
        self, client: TestClient, user: User, token: str
    ):
        to_delete = {
            'username': 'faustao',
            'email': 'fausto_e_selena@email.com',
            'senha': '1234567',
        }
        response = client.post('/contas/conta', json=to_delete)
        assert response.status_code == HTTPStatus.CREATED
        user_to_delete = response.json()
        response = client.delete(
            f'/contas/conta/{user_to_delete["id"]}',
            headers={'Authorization': f'Bearer {token}'},
        )
        assert response.status_code == HTTPStatus.UNAUTHORIZED
