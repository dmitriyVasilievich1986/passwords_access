import pytest
from passwords_access.auth import AuthText
from requests import Response


def test_parse_csrf_token():
    response = Response()
    response._content = '<input id="csrf_token" name="csrf_token" type="hidden" value="reasonable_token">'.encode()
    csrf_token = AuthText.parse_csrf_token(response)
    assert csrf_token == "reasonable_token"


def test_parse_csrf_token_value_error():
    response = Response()
    response._content = "empty_content".encode()
    with pytest.raises(ValueError):
        AuthText.parse_csrf_token(response)
