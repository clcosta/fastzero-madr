from http import HTTPStatus


def test_root_redirect_to_swagger(client):
    response = client.get('/')
    assert response.status_code == HTTPStatus.OK
    assert response.url.path == '/docs'
