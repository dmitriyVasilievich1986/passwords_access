from passwords_access import config
from passwords_access.caller import Caller
from passwords_access.dataclasses import CallerProps


def test_caller_props_url():
    caller_props = CallerProps()
    caller = Caller(caller_props)

    response = caller.get_passwords_list()
    assert response.status_code == 200
    data = response.json()

    response = caller.get_password(data["ids"][0])
    assert response.status_code == 200

    response = caller(f"{caller_props.url}{config.PASSWORDS_API}")
    assert response.status_code == 200
