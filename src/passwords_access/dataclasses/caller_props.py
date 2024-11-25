from __future__ import annotations

from dataclasses import asdict, dataclass

from .. import config


@dataclass
class CallerProps:
    username: str
    password: str
    host: str
    port: int

    def __init__(
        self,
        username: str | None = None,
        password: str | None = None,
        host: str | None = None,
        port: int | None = None,
    ) -> None:
        """
        Initialize the CallerProps object.

        Args:
            username (str, optional): The username. Defaults to None.
            password (str, optional): The password. Defaults to None.
            host (str, optional): The host. Defaults to None.
            port (int, optional): The port. Defaults to None.
        """

        self.username = username or config.USERNAME
        self.password = password or config.PASSWORD
        self.host = host or config.HOST
        self.port = port or config.PORT

    @property
    def url(self) -> str:
        """
        Returns the URL formed by combining the host and port.

        Returns:
            str: The URL formed by combining the host and port.

        Examples:
            >>> caller_props = CallerProps("user", "pass", "localhost", 80)
            >>> caller_props.url
            'http://localhost:80'
        """

        return f"http://{self.host}:{self.port}"


@dataclass
class PostData:
    username: str
    password: str
    csrf_token: str

    def json(self) -> dict:
        """
        Returns the JSON representation of the caller_props object.

        Returns:
            dict: A dictionary representing the JSON data.
        """

        return asdict(self)
