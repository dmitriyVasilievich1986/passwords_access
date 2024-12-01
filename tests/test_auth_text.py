import pytest
from passwords_access import config
from passwords_access.auth import AuthBase, AuthText
from passwords_access.dataclasses import CallerProps
from requests import Response


def test_not_implemented_error():
    caller_props = CallerProps()

    with pytest.raises(TypeError) as e:
        AuthBase(caller_props)


def test_auth_text():
    caller_props = CallerProps()
    auth = AuthText(caller_props)

    auth.cookies = None
    auth._login()

    response = auth(f"{caller_props.url}{config.PASSWORDS_API}")
    assert response.status_code == 200

    response = auth.send_request(f"{caller_props.url}{config.PASSWORDS_API}")
    assert response.status_code == 200
