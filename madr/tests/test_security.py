from datetime import datetime, timedelta

import pytest

from madr.infra import config
from madr.tools import security


def test_jwt_token():
    payload = {'user': 'Highlander'}
    token = security.create_access_token(payload)
    assert isinstance(token, str) and len(token) > 0

    res = security.get_payload_from_token(token)
    assert res['user'] == payload['user']
    expires_in = datetime.now() + timedelta(
        minutes=config.AUTH_JWT_EXPIRES_MINUTES
    )
    expires_in = expires_in.replace(microsecond=0, second=0)
    exp = datetime.fromtimestamp(res['exp'])
    exp = exp.replace(microsecond=0, second=0)
    assert exp == expires_in


def test_jwt_token_invalid_when_empty():
    with pytest.raises(type(security.CredentialException)):
        token = ''
        security.get_payload_from_token(token)


def test_jwt_token_invalid_payload_empty():
    with pytest.raises(type(security.CredentialException)):
        token = security.create_access_token({})
        security.get_payload_from_token(token)


def test_jwt_token_invalid_encode():
    with pytest.raises(type(security.CredentialException)):
        token = 'ABC'
        security.get_payload_from_token(token)
