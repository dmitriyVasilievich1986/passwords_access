from passwords_access.dataclasses import CallerProps, PostData


def test_post_data_json():
    post_data = PostData(username="user", password="pass", csrf_token="token")
    assert post_data.json() == {
        "username": "user",
        "password": "pass",
        "csrf_token": "token",
    }


def test_caller_props_url():
    caller_props = CallerProps(
        username="user", password="pass", host="localhost", port=80
    )
    assert caller_props.url == "http://localhost:80"
