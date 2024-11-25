from __future__ import annotations

from pathlib import Path

import click
from click.core import Context
from dotenv import load_dotenv
from requests import Response

from .dataclasses import CallerProps


@click.group()
@click.option("--env-file", type=Path, required=False)
@click.pass_context
def main(ctx: Context, env_file: Path | None) -> None:
    """
    Main function for accessing passwords.

    Args:
        ctx (Context): The context object.
        env_file (Path | None): The path to the environment file, if provided.
    """

    if env_file:
        load_dotenv(env_file)
    from . import config  # pylint: disable=import-outside-toplevel
    from .caller import Caller  # pylint: disable=import-outside-toplevel

    ctx.ensure_object(dict)
    cp = CallerProps(
        username=config.USERNAME,
        password=config.PASSWORD,
        host=config.HOST,
        port=config.PORT,
    )
    ctx.obj["caller"] = Caller(caller_props=cp)
    ctx.obj["url"] = cp.url


@main.command()
@click.option("--pk", required=True, type=int)
@click.pass_context
def get_password(ctx: Context, pk: str | int) -> None:
    """
    Retrieves a password based on the given ID.

    Args:
        ctx (Context): The context object.
        pk (str | int): The ID of the password to retrieve.
    """

    response: Response = ctx.obj["caller"].get_password(pk=pk)
    click.echo(response.content)


@main.command()
@click.pass_context
def get_passwords_list(ctx: Context) -> None:
    """
    Retrieves the list of passwords and prints it to the console.

    Parameters:
        ctx (Context): The click context object.
    """

    response: Response = ctx.obj["caller"].get_passwords_list()
    click.echo(response.content)
