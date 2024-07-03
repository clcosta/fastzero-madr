from http import HTTPStatus
from urllib.parse import urlencode

from fastapi.testclient import TestClient

from madr.tools.sanitize import sanitize_str


class TestCreateBook:
    def test_create_book(self, client: TestClient, token: str):
        book = {
            'ano': 1973,
            'titulo': 'Café da Manhã dos Campeões',
            'romancista_id': 1,
        }
        response = client.post(
            '/livros/livro',
            json=book,
            headers={'Authorization': f'Bearer {token}'},
        )
        assert response.status_code == HTTPStatus.CREATED
        expected_keys = {'id', 'ano', 'titulo', 'romancista_id'}
        assert expected_keys.issubset(response.json().keys())
        res_json = response.json()
        assert res_json['titulo'] == sanitize_str(book['titulo'])
        assert res_json['id'] > 0
        assert res_json['ano'] == book['ano']
        assert res_json['romancista_id'] == book['romancista_id']

    def test_create_book_invalid_token(self, client: TestClient):
        book = {
            'ano': 1973,
            'titulo': 'Café da Manhã dos Campeões',
            'romancista_id': 1,
        }
        response = client.post('/livros/livro', json=book)
        assert response.status_code == HTTPStatus.UNAUTHORIZED

    def test_create_book_invalid_data(self, client: TestClient, token: str):
        book = {
            'ano': 1,
            'titulo': '',
            'romancista_id': 'A',
        }
        response = client.post(
            '/livros/livro',
            json=book,
            headers={'Authorization': f'Bearer {token}'},
        )
        assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY

    def test_create_book_already_exists(self, client: TestClient, token: str):
        book = {
            'ano': 1962,
            'titulo': 'Como falar em público e encantar pessoas',
            'romancista_id': 2,
        }
        response = client.post(
            '/livros/livro',
            json=book,
            headers={'Authorization': f'Bearer {token}'},
        )
        assert response.status_code == HTTPStatus.CREATED
        response = client.post(
            '/livros/livro',
            json=book,
            headers={'Authorization': f'Bearer {token}'},
        )
        assert response.status_code == HTTPStatus.CONFLICT


class TestDeleteBook:
    def test_delete_book(self, client: TestClient, token: str):
        book = {
            'ano': 1936,
            'titulo': 'Como fazer amigos e influenciar pessoas',
            'romancista_id': 2,
        }
        response = client.post(
            '/livros/livro',
            json=book,
            headers={'Authorization': f'Bearer {token}'},
        )
        assert response.status_code == HTTPStatus.CREATED
        res_json = response.json()
        response = client.delete(
            f'/livros/livro/{res_json["id"]}',
            headers={'Authorization': f'Bearer {token}'},
        )
        assert response.status_code == HTTPStatus.OK
        assert response.json() == {'message': 'Livro deletado no MADR'}

    def test_delete_book_invalid_token(self, client: TestClient):
        response = client.delete('/livros/livro/1')
        assert response.status_code == HTTPStatus.UNAUTHORIZED

    def test_delete_book_not_found(self, client: TestClient, token: str):
        response = client.delete(
            '/livros/livro/0',
            headers={'Authorization': f'Bearer {token}'},
        )
        assert response.status_code == HTTPStatus.NOT_FOUND


class TestUpdatebook:
    def test_update_book(self, client: TestClient, token: str):
        book = {
            'ano': 1987,
            'titulo': 'O Alien ista',
            'romancista_id': 3,
        }
        response = client.post(
            '/livros/livro',
            json=book,
            headers={'Authorization': f'Bearer {token}'},
        )
        assert response.status_code == HTTPStatus.CREATED
        res_json = response.json()
        book['titulo'] = 'O Alienista'
        response = client.patch(
            f'/livros/livro/{res_json["id"]}',
            json=book,
            headers={'Authorization': f'Bearer {token}'},
        )
        assert response.status_code == HTTPStatus.OK
        assert response.json()['titulo'] == sanitize_str(book['titulo'])

    def test_update_book_invalid_token(self, client: TestClient):
        response = client.patch('/livros/livro/1')
        assert response.status_code == HTTPStatus.UNAUTHORIZED

    def test_update_book_not_found(self, client: TestClient, token: str):
        book = {
            'ano': 1962,
            'titulo': 'Como falar em público e encantar pessoas',
            'romancista_id': 2,
        }
        response = client.patch(
            '/livros/livro/0',
            json=book,
            headers={'Authorization': f'Bearer {token}'},
        )
        assert response.status_code == HTTPStatus.NOT_FOUND

    def test_update_book_invalid_data(self, client: TestClient, token: str):
        book = {
            'ano': 1962,
            'titulo': 'Como falar em público e encantar pessoas',
        }
        response = client.patch(
            '/livros/livro/1',
            json=book,
            headers={'Authorization': f'Bearer {token}'},
        )
        assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY

    def test_update_book_with_same_name_conflict(
        self, client: TestClient, token: str
    ):
        book = {
            'ano': 2006,
            'titulo': 'Como falar em público e encantar pessoas 2',
            'romancista_id': 2,
        }
        response = client.post(
            '/livros/livro',
            json=book,
            headers={'Authorization': f'Bearer {token}'},
        )
        assert response.status_code == HTTPStatus.CREATED
        res_json = response.json()
        response = client.patch(
            f'/livros/livro/{res_json["id"]}',
            json=book,
            headers={'Authorization': f'Bearer {token}'},
        )
        assert response.status_code == HTTPStatus.CONFLICT


class TestGetbook:
    def test_get_book(self, client: TestClient, token: str):
        book = {
            'ano': 1943,
            'titulo': 'O Pequeno Príncipe',
            'romancista_id': 4,
        }
        response = client.post(
            '/livros/livro',
            json=book,
            headers={'Authorization': f'Bearer {token}'},
        )
        assert response.status_code == HTTPStatus.CREATED
        res_json = response.json()
        response = client.get(f'/livros/livro/{res_json["id"]}')
        assert response.status_code == HTTPStatus.OK
        expected_keys = {'id', 'ano', 'titulo', 'romancista_id'}
        assert expected_keys.issubset(response.json().keys())
        assert res_json.get('id') > 0
        assert res_json == response.json()

    def test_get_book_not_found(self, client: TestClient, token: str):
        response = client.get(
            '/livros/livro/0',
            headers={'Authorization': f'Bearer {token}'},
        )
        assert response.status_code == HTTPStatus.NOT_FOUND

    def test_get_book_using_query_params_as_filters(
        self, client: TestClient, token: str
    ):
        book = {
            'ano': 1899,
            'titulo': 'Dom Casmurro',
            'romancista_id': 1,
        }
        response = client.post(
            '/livros/livro',
            json=book,
            headers={'Authorization': f'Bearer {token}'},
        )
        assert response.status_code == HTTPStatus.CREATED
        filters = urlencode({'titulo': 'casmurro'})
        response = client.get(f'/livros/livro?{filters}')
        assert response.status_code == HTTPStatus.OK
        res_json = response.json()
        assert 'livros' in res_json
        assert len(res_json['livros']) == 1

        book_2 = {
            'ano': 1899,
            'titulo': 'Coração das trevas',
            'romancista_id': 5,
        }
        response = client.post(
            '/livros/livro',
            json=book_2,
            headers={'Authorization': f'Bearer {token}'},
        )
        filters = urlencode({'ano': 1899})
        response = client.get(f'/livros/livro?{filters}')
        assert response.status_code == HTTPStatus.OK
        res_json = response.json()
        assert 'livros' in res_json
        assert len(res_json['livros']) == 2

    def test_get_book_using_unexistent_query_params(self, client: TestClient):
        filters = urlencode({'titulo': 'ABCDEFGHIJKLMNOPQRSTUVXWYZ'})
        response = client.get(f'/livros/livro?{filters}')
        assert response.status_code == HTTPStatus.OK
        res_json = response.json()
        assert res_json == {'livros': []}

    def test_pagination_on_get_book_using_query(self, client, token: str):
        book = {
            'ano': 2000,
            'titulo': 'Velozes e Furiosos',
            'romancista_id': 6,
        }
        for i in range(1, 30):
            book['titulo'] = book['titulo'] + f' {i}'
            response = client.post(
                '/livros/livro',
                json=book,
                headers={'Authorization': f'Bearer {token}'},
            )
            assert response.status_code == HTTPStatus.CREATED
        filters = urlencode({'titulo': 'velozes'})
        response = client.get(f'/livros/livro?{filters}')
        assert response.status_code == HTTPStatus.OK
        res_json_page_1 = response.json()
        assert res_json_page_1.get('livros')
        assert len(res_json_page_1['livros']) == 20

        filters = urlencode({'titulos': 'velozes', 'page': 2})
        response = client.get(f'/livros/livro?{filters}')
        assert response.status_code == HTTPStatus.OK
        res_json_page_2 = response.json()

        assert res_json_page_1['livros'] != res_json_page_2['livros']
