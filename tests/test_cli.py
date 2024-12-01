from click.testing import CliRunner
from passwords_access import config
from passwords_access.__main__ import main
from passwords_access.caller import Caller
from passwords_access.dataclasses import CallerProps


def test_cli():
    runner = CliRunner()
    caller_props = CallerProps()
    caller = Caller(caller_props)

    result = runner.invoke(main, ["get-passwords-list"])

    response = caller.get_passwords_list()
    data = response.json()

    result = runner.invoke(main, ["get-password", f'--pk={data["ids"][0]}'])
    assert result.exit_code == 0

    env_file = config.BASE_DIR / "tests/test.env"
    result = runner.invoke(
        main, [f"--env-file={env_file}", "get-password", f'--pk={data["ids"][0]}']
    )
    assert result.exit_code == 0
