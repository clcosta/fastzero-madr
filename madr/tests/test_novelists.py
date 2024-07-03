from http import HTTPStatus
from urllib.parse import urlencode

from fastapi.testclient import TestClient

from madr.tools.sanitize import sanitize_str


class TestCreateNovelist:
    def test_create_novelist(self, client: TestClient, token: str):
        novelist = {'nome': 'Clarice Lispector'}
        response = client.post(
            '/romancistas/romancista',
            json=novelist,
            headers={'Authorization': f'Bearer {token}'},
        )
        assert response.status_code == HTTPStatus.CREATED
        expected_keys = {'id', 'nome'}
        assert expected_keys.issubset(response.json().keys())
        res_json = response.json()
        assert res_json['nome'] == sanitize_str(novelist['nome'])
        assert res_json['id'] > 0

    def test_create_novelist_invalid_token(self, client: TestClient):
        novelist = {'nome': 'Clarice Lispector'}
        response = client.post('/romancistas/romancista', json=novelist)
        assert response.status_code == HTTPStatus.UNAUTHORIZED

    def test_create_novelist_invalid_data(
        self, client: TestClient, token: str
    ):
        novelist = {'nome': ''}
        response = client.post(
            '/romancistas/romancista',
            json=novelist,
            headers={'Authorization': f'Bearer {token}'},
        )
        assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY

    def test_create_novelist_already_exists(
        self, client: TestClient, token: str
    ):
        novelist = {'nome': 'Machado de Assis'}
        response = client.post(
            '/romancistas/romancista',
            json=novelist,
            headers={'Authorization': f'Bearer {token}'},
        )
        assert response.status_code == HTTPStatus.CREATED
        response = client.post(
            '/romancistas/romancista',
            json=novelist,
            headers={'Authorization': f'Bearer {token}'},
        )
        assert response.status_code == HTTPStatus.CONFLICT


class TestDeleteNovelist:
    def test_delete_novelist(self, client: TestClient, token: str):
        novelist = {'nome': 'Narcisa Amália'}
        response = client.post(
            '/romancistas/romancista',
            json=novelist,
            headers={'Authorization': f'Bearer {token}'},
        )
        assert response.status_code == HTTPStatus.CREATED
        res_json = response.json()
        response = client.delete(
            f'/romancistas/romancista/{res_json["id"]}',
            headers={'Authorization': f'Bearer {token}'},
        )
        assert response.status_code == HTTPStatus.OK
        assert response.json() == {'message': 'Romancista deletado no MADR'}

    def test_delete_novelist_invalid_token(self, client: TestClient):
        response = client.delete('/romancistas/romancista/1')
        assert response.status_code == HTTPStatus.UNAUTHORIZED

    def test_delete_novelist_not_found(self, client: TestClient, token: str):
        response = client.delete(
            '/romancistas/romancista/0',
            headers={'Authorization': f'Bearer {token}'},
        )
        assert response.status_code == HTTPStatus.NOT_FOUND


class TestUpdateNovelist:
    def test_update_novelist(self, client: TestClient, token: str):
        novelist = {'nome': 'Fagundes Dr.Vaurela'}
        response = client.post(
            '/romancistas/romancista',
            json=novelist,
            headers={'Authorization': f'Bearer {token}'},
        )
        assert response.status_code == HTTPStatus.CREATED
        res_json = response.json()
        novelist['nome'] = 'Fagundes Varela'
        response = client.patch(
            f'/romancistas/romancista/{res_json["id"]}',
            json=novelist,
            headers={'Authorization': f'Bearer {token}'},
        )
        assert response.status_code == HTTPStatus.OK
        assert response.json()['nome'] == sanitize_str(novelist['nome'])

    def test_update_novelist_invalid_token(self, client: TestClient):
        response = client.patch('/romancistas/romancista/1')
        assert response.status_code == HTTPStatus.UNAUTHORIZED

    def test_update_novelist_not_found(self, client: TestClient, token: str):
        novelist = {'nome': 'Fagundes Dr.Vaurela'}
        response = client.patch(
            '/romancistas/romancista/0',
            json=novelist,
            headers={'Authorization': f'Bearer {token}'},
        )
        assert response.status_code == HTTPStatus.NOT_FOUND

    def test_update_novelist_invalid_data(
        self, client: TestClient, token: str
    ):
        novelist = {'nome': ''}
        response = client.patch(
            '/romancistas/romancista/1',
            json=novelist,
            headers={'Authorization': f'Bearer {token}'},
        )
        assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


class TestGetNovelist:
    def test_get_novelist(self, client: TestClient, token: str):
        novelist = {'nome': 'José de Alencar'}
        response = client.post(
            '/romancistas/romancista',
            json=novelist,
            headers={'Authorization': f'Bearer {token}'},
        )
        assert response.status_code == HTTPStatus.CREATED
        res_json = response.json()
        response = client.get(f'/romancistas/romancista/{res_json["id"]}')
        assert response.status_code == HTTPStatus.OK
        assert response.json() == res_json

    def test_get_novelist_not_found(self, client: TestClient, token: str):
        response = client.get(
            '/romancistas/romancista/0',
            headers={'Authorization': f'Bearer {token}'},
        )
        assert response.status_code == HTTPStatus.NOT_FOUND

    def test_get_novelist_using_query_params_as_filters(
        self, client: TestClient, token: str
    ):
        novelist = {'nome': 'Casimiro de Abreu'}
        response = client.post(
            '/romancistas/romancista',
            json=novelist,
            headers={'Authorization': f'Bearer {token}'},
        )
        assert response.status_code == HTTPStatus.CREATED
        filters = urlencode({'nome': 'casimiro'})
        response = client.get(f'/romancistas/romancista?{filters}')
        assert response.status_code == HTTPStatus.OK
        res_json = response.json()
        assert res_json.get('romancistas')
        assert len(res_json['romancistas']) == 1

    def test_get_novelist_using_unexistent_query_params(
        self, client: TestClient
    ):
        filters = urlencode({'nome': 'ABCDEFGHIJKLMNOPQRSTUVXWYZ'})
        response = client.get(f'/romancistas/romancista?{filters}')
        assert response.status_code == HTTPStatus.OK
        res_json = response.json()
        assert res_json == {'romancistas': []}

    def test_pagination_on_get_novelist_using_query(self, client, token: str):
        novelist = {'nome': 'Romancista'}
        for i in range(1, 30):
            novelist['nome'] = novelist['nome'] + f' {i}'
            response = client.post(
                '/romancistas/romancista',
                json=novelist,
                headers={'Authorization': f'Bearer {token}'},
            )
            assert response.status_code == HTTPStatus.CREATED
        filters = urlencode({'nome': 'romancista'})
        response = client.get(f'/romancistas/romancista?{filters}')
        assert response.status_code == HTTPStatus.OK
        res_json = response.json()
        assert res_json.get('romancistas')
        assert len(res_json['romancistas']) == 20
