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
            )
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
